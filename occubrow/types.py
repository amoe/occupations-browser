# Shims for NPD types to enable mocking
# "Don't mock what you don't own".

class Node(object):
    id_ = None
    properties = None

    def __init__(self, id_, properties):
        """
        Initialize a Node with a numerical ID and a dictionary of properties.
        """
        self.id_ = id_
        self.properties = properties

    def get_id(self):
        return self.id_
    
    def get_properties(self):
        return self.properties


class Relationship(object):
    start_node = None
    end_node = None
    properties = None
    type_ = None

    def __init__(self, start_node, end_node, properties, type_):
        """
        Initialize a Relationship.  Start node and end node are numerical
        node IDs.  The list of properties is a dictionary.  The node type
        is specified as a string.
        """
        self.start_node = start_node
        self.end_node = end_node
        self.properties = properties
        self.type_ = type_

    def get_start_node(self):
        return self.start_node

    def get_end_node(self):
        return self.end_node

    def get_properties(self):
        return self.properties

    def get_type(self):
        return self.type_
