import networkx
import neo4j_apoc_tree
import misc
import pprint
import json
import pytest
from logging import debug
import neo4j_test_utility

EXPECTED_TAXONOMY_RESULT = {'_type': 'Taxon',
                            'children': [{'_type': 'Taxon',
                                          'children': [{'_type': 'Taxon',
                                                        'id': 21003,
                                                        'name': 'Aurelia labiata'},
                                                       {'_type': 'Taxon',
                                                        'id': 20987,
                                                        'name': 'Aurelia aurita'}],
                                          'id': 20986,
                                          'name': 'Aurelia'},
                                         {'_type': 'Taxon',
                                          'children': [{'_type': 'Taxon',
                                                        'id': 20988,
                                                        'name': 'Deepstaria reticulum'},
                                                       {'_type': 'Taxon',
                                                        'id': 21004,
                                                        'name': 'Deepstaria enigmatica'}],
                                          'id': 21002,
                                          'name': 'Deepstaria'}],
                            'id': 20985,
                            'name': 'Ulmaridae'}


@pytest.fixture(scope='function')
def neo4j_fixture():
    debug("setting up neo4j")
    return 42


def test_taxonomy_1(neo4j_fixture):
    debug("neo4j_fixture = %s", repr(neo4j_fixture))
    dg = neo4j_apoc_tree.get_tree(neo4j_apoc_tree.TAXONOMY_TREE_QUERY, 'supercategory_of')
    root = next(networkx.topological_sort(dg))

    # This is just the default tree-json format, but we prefer to be explicit 
    # about it
    attrs = {
        'children': 'children',
        'id': 'id'
    }
    dg_formatted_as_tree = networkx.tree_data(
        dg, root=root, attrs=attrs
    )
    assert dg_formatted_as_tree == EXPECTED_TAXONOMY_RESULT
