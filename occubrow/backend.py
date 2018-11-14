import neo4j
import networkx
import networkx.readwrite.json_graph
from occubrow.drawing import quickplot
import operator
import occubrow.errors
from logging import debug

# XXX SRP
import nltk
import string

ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

# Preprocessing step to strip punctuation, terrible
def strip_punctuation(tokens):
    return [
        t for t in tokens if t not in string.punctuation
    ]


# Rebuild the graph in memory, converting from the NPD wrapper structures
# to Networkx structures
def rebuild_graph(results):
    g = networkx.DiGraph()

    for node in results['nodes']:
        merged_node_properties = {'label': node.get_label()}
        merged_node_properties.update(node.get_properties())

        g.add_node(
            node.get_id(), **merged_node_properties
        )

    for rel in results['rels']:
        g.add_edge(
            rel.get_start_node(),
            rel.get_end_node(),
            **rel.get_properties(),
            type=rel.get_type()
        )

    return g

# Not actually tested but this property should definitely hold true.
def check_round_trip():
    g1 = rebuild_graph(pull_graph())
    data = networkx.readwrite.json_graph.node_link_data(g1)
    g2 = networkx.readwrite.json_graph.node_link_graph(data)
    return strict_eq(g1, g2)


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

# This is primarily used for testing, and obviously a UUID used in an
# integration test won't be identical, so we have to ignore them
def node_match(n1, n2):
    ignored_keys_set = {'uuid'}

    return operator.eq(
        without_keys(n1, ignored_keys_set),
        without_keys(n2, ignored_keys_set)
    )

def strict_eq(g1, g2):
    return networkx.is_isomorphic(g1, g2, node_match=node_match, edge_match=operator.eq)

class OccubrowBackend(object):
    def __init__(self, repository):
        self.repository = repository

    def add_sentence(self, sentence):
        pass

    def export_graph(self):
        return networkx.readwrite.json_graph.node_link_data(
            rebuild_graph(self.repository.pull_graph())
        )

    def graph_matches(self, data):
        return strict_eq(
            rebuild_graph(self.repository.pull_graph()), 
            networkx.readwrite.json_graph.node_link_graph(data)
        )

    def export_taxonomy_tree(self, root):
        """
        Export the taxonomy tree in a JSON-able format.  Should be interpretable
        by d3-hierarchy, networkx, and the JavaScript TreeModel library.

        Root is a string that specifies the 'content' property of a Taxon node
        with in-degree zero.  That is, root is a string that uniquely names the
        'top' Taxon of a taxonomy.  If the database contains two taxonomies
        with a top-node with the same value for 'content', the behaviour is
        undefined (i.e. this should never happen and is considered a corruption).
        """
        result = self.repository.pull_all_taxonomies()
        g = rebuild_graph(result)
        return networkx.tree_data(g, root)
                
    def import_taxonomy(self, taxonomy_data):
        """
        Import taxonomy data.  Data should be a JSON tree (in the sense defined
        by networkx).
        """
        if not taxonomy_data:
            raise occubrow.errors.EmptyTaxonomyError()

        if not 'id' in taxonomy_data:
            raise occubrow.errors.EmptyTaxonomyError()

        g = networkx.readwrite.json_graph.tree_graph(taxonomy_data)

        for node in g.nodes:
            self.repository.run_statement("""
                 CREATE (t:Taxon {content: $content})
            """.strip(), content=node)

        for edge in g.edges:
            start_node = edge[0]
            end_node = edge[1]

            self.repository.run_statement("""
                MATCH (t1:Taxon {content: $start_node}), (t2:Taxon {content: $end_node})
                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)
            """.strip(), start_node=start_node, end_node=end_node)


    def add_sentence(self, sentence):
        """
        Add a single sentence.  Sentence is a flat text string which will be
        tokenized.  It's assumed that this is the result of a previous
        sentence-tokenization step (i.e. it's not a giant flat body of text.)
        Returns the sentence UUID.
        """
        # tokenize step goes here
        tokens = strip_punctuation(nltk.word_tokenize(sentence))
        sentence_uuid = self.repository.add_sentence_with_tokens(tokens)
        self.repository.add_precedes_links(tokens)
        return sentence_uuid
