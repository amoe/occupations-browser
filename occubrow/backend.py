import neo4j
import networkx
import networkx.readwrite.json_graph
from occubrow.drawing import quickplot
import operator
import occubrow.errors
from logging import debug
import occubrow.queries
import json
import datetime
import pdb

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
    ignored_keys_set = {}

    return operator.eq(
        without_keys(n1, ignored_keys_set),
        without_keys(n2, ignored_keys_set)
    )

def roundtrip(g):
    return networkx.node_link_graph(networkx.node_link_data(g))

# No idea why but the serialization here seems necessary.  Spurious results
# otherwise.
def strict_eq(g1, g2):
    return networkx.is_isomorphic(
        roundtrip(g1), roundtrip(g2),
        node_match=node_match, edge_match=operator.eq
    )

def find_root_by_content(g, wanted):
   sources = [v for v, indegree in g.in_degree() if indegree == 0]
   valid_sources = [n for n, content in g.nodes(data='content') if content == wanted]

   if not valid_sources:
       raise occubrow.errors.NoRootsFoundError()

   if len(valid_sources) != 1:
       raise occubrow.errors.AmbiguousRootError()

   return valid_sources[0]


class OccubrowBackend(object):
    def __init__(self, repository, identifier_function):
        self.repository = repository
        self.identifier_function = identifier_function

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
        result = self.repository.get_all_taxonomies()
        g = rebuild_graph(result)
        root_id = find_root_by_content(g, root)
        return networkx.tree_data(g, root_id)
                
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
        sentence_uuid = self.add_sentence_with_tokens(tokens)
        self.repository.add_precedes_links(tokens)
        return sentence_uuid

    def add_sentence_with_tokens(self, phrase):
        """
        Add a Sentence node plus its contained Token links, which will be
        merged.  Phrase should be a tokenized list.  Returns a new uuid that
        can be used to locate the Sentence.
        """
        this_uuid = self.identifier_function()

        self.repository.run_statement(
            occubrow.queries.CREATE_SENTENCE_QUERY,
            sentence=phrase, uuid=str(this_uuid)
        )

        for index, token in enumerate(phrase):
            relationship_properties = {
                'index': index
            }

            if index == 0:
                relationship_properties['firstIndex'] = True

            if index == len(phrase) - 1:
                relationship_properties['lastIndex'] = True


            self.repository.run_statement(
                occubrow.queries.CREATE_TOKEN_QUERY, token=token
            )
            self.repository.run_statement(
                occubrow.queries.CREATE_CONTAINS_RELATIONSHIP,
                token=token, 
                sentence_id=str(this_uuid),
                relationship_properties=relationship_properties
            )

        return this_uuid

    
    def create_compound(self, tokens):
        new_compound_id = self.identifier_function()
        result = self.repository.run_statement(
            occubrow.queries.CREATE_COMPOUND_NODE_QUERY, {'id': new_compound_id}
        )
        assert result.summary().counters.nodes_created == 1

        for token in tokens:
            result = self.repository.run_statement(
                occubrow.queries.CREATE_COMPOUND_NODE_LINKED_TOKENS,
                {'search_id': new_compound_id, 'search_content': token}
            )
            assert result.summary().counters.relationships_created == 1


        return new_compound_id

    def dump_internal_graph(self):
        self.dump_graph(self.export_graph())

    def dump_graph(self, data):
        with open('/tmp/export-%s.json' % datetime.datetime.utcnow(), 'w') as f:
            json.dump(data, f, indent=4)
