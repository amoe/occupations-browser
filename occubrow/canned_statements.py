import occubrow.queries

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


class CreateCompoundNodeQuery(CannedStatement):
    def __init__(self, id_):
        self.id_ = id_

    def get_cypher(self):
        return occubrow.queries.CREATE_COMPOUND_NODE_QUERY

    def get_parameters(self):
        return {'id': self.id_}


class CreateCompoundLink(CannedStatement):
    def __init__(self, compound_id, search_token):
        self.compound_id = compound_id
        self.search_token = search_token

    def get_cypher(self):
        return occubrow.queries.CREATE_COMPOUND_NODE_LINKED_TOKENS

    def get_parameters(self):
        return {
            'search_id': self.compound_id, 'search_content': self.search_token
        }
