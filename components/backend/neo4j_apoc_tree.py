import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools
import misc
import pprint

# relationship_name here is 'precedes'
APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

# relationship_name here is 'supercategory_of'
TAXONOMY_TREE_QUERY = """
    MATCH p = (ta1:Taxon)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
    WHERE NOT (ta2)-[:SUPERCATEGORY_OF]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value;
"""


def tree_to_graph(tree, relationship_name):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children=relationship_name)
    return networkx.tree_graph(tree, object_format)

def get_tree(query, relationship_name):
    result = misc.run_some_query(query, {})
    paths = result.value()
    get_graph = lambda p: tree_to_graph(p, relationship_name)
    return functools.reduce(networkx.compose, map(get_graph, paths))

if __name__ == '__main__':
    tree = get_taxonomy_tree()
    print(tree.nodes)
    # blah = networkx.tree_data(tree, root=)
    # print(blah)
