import networkx
import neo4j_apoc_tree
import pprint
import json
import pytest
from logging import debug
import neo4j_test_utility

EXPECTED_TAXONOMY_RESULT = {'_type': 'Taxon',
 'children': [{'_type': 'Taxon',
                'children': [{'_type': 'Taxon',
                               'id': 20717,
                               'name': 'Aurelia labiata'},
                              {'_type': 'Taxon',
                               'id': 20718,
                               'name': 'Aurelia aurita'}],
                'id': 20715,
                'name': 'Aurelia'},
               {'_type': 'Taxon',
                'children': [{'_type': 'Taxon',
                               'id': 20720,
                               'name': 'Deepstaria reticulum'},
                              {'_type': 'Taxon',
                               'id': 20719,
                               'name': 'Deepstaria enigmatica'}],
                'id': 20716,
                'name': 'Deepstaria'}],
 'id': 20714,
 'name': 'Ulmaridae'}



@pytest.fixture(scope='function')
def neo4j_fixture():
    debug("setting up neo4j")
    neo4j_test_utility.clear_all()
    neo4j_test_utility.add_taxonomy()
    return 42

def test_taxonomy_1(neo4j_fixture):
    debug("neo4j_fixture = %s", repr(neo4j_fixture))

    obj = neo4j_apoc_tree.Neo4jRepository()

    dg = obj.get_tree(neo4j_apoc_tree.TAXONOMY_TREE_QUERY, 'supercategory_of')

    # This essentially gets the (assumed to be single!) root of the tree.
    try:
        root = next(networkx.topological_sort(dg))
    except StopIteration as e:
        raise Exception("empty taxonomy?") from e

    # This is just the default tree-json format, but we prefer to be explicit 
    # about it
    attrs = {
        'children': 'children',
        'id': 'id'
    }
    dg_formatted_as_tree = networkx.tree_data(
        dg, root=root, attrs=attrs
    )

    expected_graph = networkx.tree_graph(EXPECTED_TAXONOMY_RESULT, dict(id='id', children='children'))
    reparsed_graph = networkx.tree_graph(dg_formatted_as_tree, dict(id='id', children='children'))

    # is_isomorphic will automatically ignore the id numbers.  Note that you
    # can provide node_match function to override matching behaviour.  We don't
    # need to do so here
    assert networkx.is_isomorphic(reparsed_graph, expected_graph)

    
