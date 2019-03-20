import neo4j
import networkx
import networkx.readwrite.json_graph
import occubrow.errors as errors
from occubrow.utility \
  import get_node_by_attribute, dfs_tree_with_node_attributes, is_null_graph
from occubrow.drawing import quickplot
from occubrow.canned_statements \
  import CreateCompoundNodeQuery, CreateCompoundLink, CreateGroupLink, \
         CreateGroupNodeQuery, ClearAllDataQuery, AddAnnotationStatement, \
         GetEntireGraphQuery, GetEntireTokenGraphQuery, SlurpTaxonomiesQuery, \
         GetTokenTreeQuery, GetRandomTokenQuery, GetTaxonomyRootsQuery, \
         GetTokenRootWithTaxonFilterQuery, GetContextsQuery, GetMetricsQuery, \
         SearchTokensQuery, GetAllTokensQuery, GetCentralityQuery, \
         RegisterStopWordQuery, LookupTaxonQuery
import operator
from logging import debug
import occubrow.queries
import json
import datetime
import pdb
import nltk
import string
import pprint

# Used by get_token_tree, this should transform to the format 'TokenDatum'
# defined in occubrow-graph-view's interfaces.ts file.
def transform(g):
    result = networkx.DiGraph()

    result.add_nodes_from(g.nodes(data=True))
    for u, v, ddict in g.edges(data=True):
        if ddict['type'] == 'PRECEDES':
            result.nodes[v]['strength'] = ddict['occurrences']

    result.add_edges_from(g.edges)

    return result

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
        u = rel.get_start_node()
        v = rel.get_end_node()

        # skip invalid rels that can come from some queries
        if not (u in g and v in g):
            continue

        g.add_edge(
            rel.get_start_node(),
            rel.get_end_node(),
            **rel.get_properties(),
            type=rel.get_type()
        )

    return g

# Not actually tested but this property should definitely hold true.
def check_round_trip():
    g1 = rebuild_graph(pull_graph(GetEntireGraphQuery()))
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

def find_roots(g):
    return [v for v, indegree in g.in_degree() if indegree == 0]

def find_root_by_content(g, wanted):
   sources = [v for v, indegree in g.in_degree() if indegree == 0]
   valid_sources = [n for n, content in g.nodes(data='content') if content == wanted]

   if not valid_sources:
       raise errors.NoRootsFoundError()

   if len(valid_sources) != 1:
       raise errors.AmbiguousRootError()

   return valid_sources[0]


class OccubrowBackend(object):
    def __init__(self, repository, identifier_function, micromacro_gateway):
        self.repository = repository
        self.identifier_function = identifier_function
        self.micromacro_gateway = micromacro_gateway

    def get_taxonomy_roots(self):
        result = self.repository.run_canned_statement(GetTaxonomyRootsQuery())
        return [
            {'uri': n['uri'], 'content': n['content']}
            for n in result.value('ta')
        ]

    def export_graph(self):
        return networkx.readwrite.json_graph.node_link_data(
            rebuild_graph(self.repository.pull_graph(GetEntireGraphQuery()))
        )

    def graph_matches(self, data):
        return strict_eq(
            rebuild_graph(self.repository.pull_graph(GetEntireGraphQuery())),
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
        result = self.repository.pull_graph(SlurpTaxonomiesQuery())
        g = rebuild_graph(result)
        root_id = find_root_by_content(g, root)
        tree = dfs_tree_with_node_attributes(g, root_id, depth_limit=None)
        return networkx.tree_data(tree, root_id)
                
    def import_taxonomy(self, taxonomy_data):
        """
        Import taxonomy data.  Data should be a JSON tree (in the sense defined
        by networkx).
        """
        if not taxonomy_data:
            raise errors.EmptyTaxonomyError()

        if not 'id' in taxonomy_data:
            raise errors.EmptyTaxonomyError()

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


    def preprocess(self, sentence):
        return strip_punctuation(nltk.word_tokenize(sentence))

    def add_sentence(self, sentence):
        """
        Add a single sentence.  Sentence is a flat text string which will be
        tokenized.  It's assumed that this is the result of a previous
        sentence-tokenization step (i.e. it's not a giant flat body of text.)
        Returns the sentence UUID.
        """
        # tokenize step goes here
        tokens = self.preprocess(sentence)
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

    def clear_all_data(self):
        self.repository.run_canned_statement(ClearAllDataQuery())

    def create_group(self, tokens):
        new_group_id = self.identifier_function()
        result = self.repository.run_canned_statement(
            CreateGroupNodeQuery(new_group_id)
        )
        assert result.summary().counters.nodes_created == 1

        for token in tokens:
            result = self.repository.run_canned_statement(
                CreateGroupLink(new_group_id, token)
            )
            assert result.summary().counters.relationships_created == 1

        return new_group_id
    
    def create_compound(self, tokens):
        new_compound_id = self.identifier_function()

        result = self.repository.run_canned_statement(
            CreateCompoundNodeQuery(new_compound_id)
        )
        assert result.summary().counters.nodes_created == 1

        for token in tokens:
            result = self.repository.run_canned_statement(
                CreateCompoundLink(new_compound_id, token)
            )
            assert result.summary().counters.relationships_created == 1


        return new_compound_id

    def dump_internal_graph(self):
        self.dump_graph(self.export_graph())

    def dump_graph(self, data):
        with open('/tmp/export-%s.json' % datetime.datetime.utcnow(), 'w') as f:
            json.dump(data, f, indent=4)

    def get_token_tree(self, token, depth_limit, cooccurrence_threshold):
        # Basic strategy is to pull the entire tree, which can be memory
        # intensive, and then to dfs_tree it to get the specific tree.
        g = rebuild_graph(self.repository.pull_graph(GetTokenTreeQuery(token, depth_limit, cooccurrence_threshold)))

        print(g.number_of_nodes())
        print(g.number_of_edges())

        if g.number_of_nodes() == 0:
            raise Exception('Result tree was empty? 1')

        # At this stage the occurrence properties should have been migrated to
        # in memory graph.  However they won't appear on the tree export yet.

        # So, migrate the strength attributes correctly.
        g2 = transform(g)

        root = get_node_by_attribute(g2, 'content', token)
        g2.nodes[root]['strength'] = None
        tree = dfs_tree_with_node_attributes(g2, root, depth_limit=depth_limit)

        print("Number of nodes in tree", tree.number_of_nodes())
        print("Number of edges in tree", tree.number_of_edges())

        return networkx.tree_data(tree, root)


    def annotate(self, sentence_id, token, taxon_reference):
        """
        Create an annotation.  Sentence ID is a uuid.  Token is the actual token
        which must be unique.  Taxon reference is the tag URI of a taxon.
        You must trim the token first.
        """

        # basic strategy is to match the taxon through URI.  Match token by
        # the token.  Sentence id will just be a property of the link.
        result = self.repository.run_canned_statement(
            AddAnnotationStatement(sentence_id, token, taxon_reference)
        )
        if result.summary().counters.relationships_created != 1:
            raise errors.AnnotationNotCreatedError(token, taxon_reference)
    

    def get_metrics(self):
        r = self.repository.run_canned_statement(GetMetricsQuery())
        return r.data()[0]

    def pick_root(self):
        result = self.repository.run_canned_statement(GetRandomTokenQuery())
        return result.single().value('t')['content']

    # sparse tree with taxon
    def search_with_taxons(self, token, taxon_uris, depth_limit, cooccurrence_threshold):
        g = rebuild_graph(
            self.repository.pull_graph(
                GetTokenRootWithTaxonFilterQuery(
                    token, taxon_uris, depth_limit, cooccurrence_threshold
                )
            )
        )

        # if the graph is empty then nothing was matched.  re-add the root
        # node
        if is_null_graph(g):
            g.add_node(0, content=token)

        # now reconnect the graph
        root = get_node_by_attribute(g, 'content', token)
        for node in g.nodes:
            g.nodes[node]['strength'] = 0
            if node != root: g.add_edge(root, node)
            
        g.nodes[root]['strength'] = None

        return networkx.tree_data(g, root)

    def get_contexts(self, token):
        result = self.repository.run_canned_statement(GetContextsQuery(token))
        return [
            {'uuid': n['uuid'],
             'content': n['content']}
             for n in result.value('s')
        ]
        

    def get_all_tokens(self):
        result = self.repository.run_canned_statement(GetAllTokensQuery())
        return [r['content'] for r in result]
        
    def search_tokens(self, substring):
        result = self.repository.run_canned_statement(SearchTokensQuery(substring))
        return [r['content'] for r in result]

    def get_centrality_statistics(self):
        result = self.repository.run_canned_statement(GetCentralityQuery('DESC'))
        return result.data()

    def register_stop_word(self, token):
        result = self.repository.run_canned_statement(RegisterStopWordQuery(token))
        return result

    def get_taxon_by_content(self, content, key):
        result = self.repository.run_canned_statement(LookupTaxonQuery(content, key))
        uri = result.value('uri')

        if len(uri) == 0:
            return None

        if len(uri) != 1:
            raise errors.AmbiguousTaxonException(content)

        return uri[0]

    def query_micromacro(self, query_spec):
        return self.micromacro_gateway.query(query_spec)
