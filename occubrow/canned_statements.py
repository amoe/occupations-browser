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
