import neo4j
import neo4j.v1
import networkx
import matplotlib
import matplotlib.pyplot
import functools
import misc

APOC_TREE_GENERATOR_QUERY = """
    MATCH p = (:Token {content: "the"})-[:PRECEDES*]->(end:Token) 
    WHERE NOT (end)-[:PRECEDES]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value
"""

TAXONOMY_TREE_QUERY = """
    MATCH p = (ta1:Taxon)-[:SUPERCATEGORY_OF*]->(ta2:Taxon)
    WHERE NOT (ta2)-[:SUPERCATEGORY_OF]->()
    CALL apoc.convert.toTree([p]) YIELD value
    RETURN value;
"""


def tree_to_graph(tree):
    # defined by apoc, precedes is based on the relationship label
    object_format = dict(id='_id', children='precedes')
    return networkx.tree_graph(tree, object_format)

def getgraphs():
    result = misc.run_some_query(APOC_TREE_GENERATOR_QUERY, {})
    paths = result.value()

    return functools.reduce(networkx.compose, map(tree_to_graph, paths))

# I really think that this should work but for some reason it just doesn't
def get_taxonomy_tree():
    result = misc.run_some_query(TAXONOMY_TREE_QUERY, {})
    paths = result.value()
    return functools.reduce(networkx.compose, map(tree_to_graph, paths))

if __name__ == '__main__':
    tree = get_taxonomy_tree()
    print(tree.nodes)
    # blah = networkx.tree_data(tree, root=)
    # print(blah)
