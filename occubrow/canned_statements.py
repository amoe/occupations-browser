# canned statements know how to marshal themselves to a string that can be
# provided to the N-P-D driver, but also can be interrogated for their
# various values in a sensible way, and are also immutable in spirit

class CannedStatement(object):
    def __init__(self):
        raise Exception("not implemented")
    
    # allow comparing these items by their respective attribute dictionaries
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def get_cypher(self):
        raise Exception("not implemented")

    def get_parameters(self):
        raise Exception("not implemented")


CREATE_COMPOUND_NODE_QUERY = """
    CREATE (c:Compound {uuid: {id}})
"""

class CreateCompoundNodeQuery(CannedStatement):
    def __init__(self, id_):
        self.id_ = id_

    def get_cypher(self):
        return CREATE_COMPOUND_NODE_QUERY

    def get_parameters(self):
        return {'id': self.id_}


CREATE_COMPOUND_NODE_LINKED_TOKENS = """
    MATCH (c:Compound {uuid: {search_id}}), (t:Token {content: {search_content}})
    CREATE (c)-[:COMPOUND_CONTAINS]->(t);
"""

class CreateCompoundLink(CannedStatement):
    def __init__(self, compound_id, search_token):
        self.compound_id = compound_id
        self.search_token = search_token

    def get_cypher(self):
        return CREATE_COMPOUND_NODE_LINKED_TOKENS

    def get_parameters(self):
        return {
            'search_id': self.compound_id, 'search_content': self.search_token
        }


CREATE_GROUP_NODE_QUERY = """
    CREATE (g:Group {uuid: {id}})
"""

class CreateGroupNodeQuery(CannedStatement):
    def __init__(self, id_):
        self.id_ = id_

    def get_cypher(self):
        return CREATE_GROUP_NODE_QUERY

    def get_parameters(self):
        return {'id': self.id_}

CREATE_GROUP_LINK_QUERY = """
    MATCH (c:Group {uuid: {search_id}}), (t:Token {content: {search_content}})
    CREATE (c)-[:GROUP_CONTAINS]->(t);
"""

class CreateGroupLink(CannedStatement):
    def __init__(self, group_id, search_token):
        self.group_id = group_id
        self.search_token = search_token

    def get_cypher(self):
        return CREATE_GROUP_LINK_QUERY

    def get_parameters(self):
        return {
            'search_id': self.group_id,
            'search_content': self.search_token
        }


CLEAR_ALL_DATA_QUERY = """
    MATCH (n) DETACH DELETE n;
"""

class ClearAllDataQuery(CannedStatement):
    def __init__(self):
        pass

    def get_cypher(self):
        return CLEAR_ALL_DATA_QUERY

    def get_parameters(self):
        return {}

ADD_ANNOTATION_QUERY = """
    MATCH (to:Token {content: {token}}),
          (ta:Taxon {uri: {taxon_reference}}),
          (s:Sentence {uuid: {sentence_id}})
    CREATE (to)-[:INSTANCE_OF {context: {sentence_id}}]->(ta)
"""

class AddAnnotationStatement(CannedStatement):
    def __init__(self, sentence_id, token, taxon_reference):
        self.sentence_id = sentence_id
        self.token = token
        self.taxon_reference = taxon_reference

    def get_cypher(self):
        return ADD_ANNOTATION_QUERY

    def get_parameters(self):
        return {
            'sentence_id': self.sentence_id,
            'token': self.token,
            'taxon_reference': self.taxon_reference
        }


GET_ENTIRE_GRAPH_QUERY = """
    MATCH ()-[r]->()
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

class GetEntireGraphQuery(CannedStatement):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_ENTIRE_GRAPH_QUERY

    def get_parameters(self):
        return {}


GET_ENTIRE_TOKEN_GRAPH_QUERY = """
    MATCH (t1:Token)-[r]->(t2:Token)
    WITH COLLECT(r) AS rels
    MATCH (n)
    RETURN rels, COLLECT(n) AS nodes
"""

class GetEntireTokenGraphQuery(CannedStatement):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_ENTIRE_TOKEN_GRAPH_QUERY

    def get_parameters(self):
        return {}


SLURP_TAXONOMIES_QUERY = """
    MATCH (t1:Taxon)-[r]->(t2:Taxon)
    WITH COLLECT(r) AS rels
    MATCH (t:Taxon)
    RETURN rels, COLLECT(t) AS nodes
"""

class SlurpTaxonomiesQuery(CannedStatement):
    def __init__(self):
        pass

    def get_cypher(self):
        return SLURP_TAXONOMIES_QUERY

    def get_parameters(self):
        return {}



GET_TOKEN_TREE_QUERY_TEMPLATE = """
MATCH (to1:Token {content: {root}})
OPTIONAL MATCH path = (to1)-[r:PRECEDES*..%d]->(to2:Token)
WHERE all(rel in relationships(path) WHERE rel.occurrences > 0)
RETURN (COLLECT(to1) + COLLECT(to2)) AS nodes, COLLECT(last(r)) AS rels
"""

class GetTokenTreeQuery(CannedStatement):
    def __init__(self, root, depth_limit):
        self.root = root
        self.depth_limit = depth_limit

    def get_cypher(self):
        # Not the safest thing ever but this will die with TypeError on 
        # injection attempts anyway
        return GET_TOKEN_TREE_QUERY_TEMPLATE % (self.depth_limit,)

    def get_parameters(self):
        return {'root': self.root}


# fast and wrong query
GET_RANDOM_TOKEN_QUERY = """
    MATCH (t:Token) WITH t WHERE rand() < 0.3 RETURN t LIMIT 1
"""

class GetRandomTokenQuery(CannedStatement):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_RANDOM_TOKEN_QUERY

    def get_parameters(self):
        return {}
    



GET_TAXONOMY_ROOTS_QUERY = """
    MATCH (ta:Taxon) WHERE NOT (ta)<-[:SUPERCATEGORY_OF]-(:Taxon) RETURN ta
"""

class GetTaxonomyRootsQuery(object):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_TAXONOMY_ROOTS_QUERY

    def get_parameters(self):
        return {}


GET_TOKEN_ROOT_WITH_TAXON_FILTER_QUERY = """
MATCH (ta1:Taxon)
OPTIONAL MATCH (ta1)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
WHERE ta1.uri IN {taxon_uri_list}
WITH {taxon_uri_list} + COLLECT(ta2.uri) AS validTaxonUris
MATCH (to1:Token {content: {wanted_token}}), (to1)-[r:PRECEDES*..%d]->(to2:Token), (to2)-[:INSTANCE_OF]->(ta:Taxon)
WHERE ta.uri IN validTaxonUris
RETURN COLLECT(to1) + COLLECT(to2) AS nodes, [] AS rels
"""

class GetTokenRootWithTaxonFilterQuery(object):
    def __init__(self, token, taxon_uri_list, depth_limit):
        self.token = token
        self.taxon_uri_list = taxon_uri_list
        self.depth_limit = depth_limit

    def get_cypher(self):
        return GET_TOKEN_ROOT_WITH_TAXON_FILTER_QUERY % self.depth_limit

    def get_parameters(self):
        return {
            'wanted_token': self.token,
            'taxon_uri_list': self.taxon_uri_list
        }
    

GET_CONTEXTS_QUERY = """
MATCH (to:Token {content: {wanted_token}})<-[:CONTAINS]-(s:Sentence)
RETURN s
"""

class GetContextsQuery(object):
    def __init__(self, token):
        self.token = token

    def get_cypher(self):
        return GET_CONTEXTS_QUERY

    def get_parameters(self):
        return {
            'wanted_token': self.token
        }

GET_METRICS_QUERY = """
MATCH (n)
WITH COUNT(n) AS order
MATCH ()-[r]->()
RETURN order, COUNT(r) AS size
"""

class GetMetricsQuery(object):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_METRICS_QUERY

    def get_parameters(self):
        return {}

SEARCH_TOKENS_QUERY = """
MATCH (t:Token)
WHERE toLower(t.content) CONTAINS toLower({substring})
RETURN t.content AS content
ORDER BY toLower(t.content) ASC
"""

class SearchTokensQuery(object):
    def __init__(self, substring):
        self.substring = substring

    def get_cypher(self):
        return SEARCH_TOKENS_QUERY

    def get_parameters(self):
        return {
            'substring': self.substring
        }

GET_ALL_TOKENS_QUERY = """
MATCH (t:Token)
RETURN t.content AS content
ORDER BY toLower(t.content) ASC
"""

class GetAllTokensQuery(object):
    def __init__(self):
        pass

    def get_cypher(self):
        return GET_ALL_TOKENS_QUERY

    def get_parameters(self):
        return {}

GET_CENTRALITY_QUERY = """
MATCH (st:StopWord)
WITH COLLECT(st.content) as stopWords
CALL algo.closeness.stream('Token', 'PRECEDES')
YIELD nodeId, centrality
WITH algo.getNodeById(nodeId).content as token, centrality
WHERE NOT token in stopWords
RETURN token AS node, centrality
ORDER BY centrality %s
LIMIT 10;
"""

class GetCentralityQuery(object):
    def __init__(self, direction):
        if direction == 'DESC' or direction == 'ASC':
            self.direction = direction
        else:
            raise Exception('invalid direction')

    def get_cypher(self):
        return GET_CENTRALITY_QUERY % self.direction

    def get_parameters(self):
        return {}

REGISTER_STOP_WORD_QUERY = """
MERGE (st:StopWord {content: {token}});
"""

class RegisterStopWordQuery(object):
    def __init__(self, token):
        self.token = token

    def get_cypher(self):
        return REGISTER_STOP_WORD_QUERY

    def get_parameters(self):
        return {'token': self.token}


LOOKUP_TAXON_QUERY = """
    MATCH (ta:Taxon {content: {wanted_content}, key: {key}}) RETURN ta.uri AS uri
"""

class LookupTaxonQuery(object):
    def __init__(self, wanted_content, key):
        self.wanted_content = wanted_content
        self.key = key

    def get_cypher(self):
        return LOOKUP_TAXON_QUERY

    def get_parameters(self):
        return {'wanted_content': self.wanted_content,
                'key': self.key}
        
