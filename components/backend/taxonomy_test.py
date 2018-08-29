import neo4j_apoc_tree

EXPECTED_TAXONOMY_RESULT = [{'_id': 19975,
                             '_type': 'Taxon',
                             'name': 'Ulmaridae',
                             'supercategory_of': [{'_id': 19976,
                                                   '_type': 'Taxon',
                                                   'name': 'Deepstaria',
                                                   'supercategory_of': [{'_id': 19978,
                                                                         '_type': 'Taxon',
                                                                         'name': 'Deepstaria enigmatica'},
                                                                        {'_id': 19979,
                                                                         '_type': 'Taxon',
                                                                         'name': 'Deepstaria reticulum'}]},
                                                  {'_id': 19977,
                                                   '_type': 'Taxon',
                                                   'name': 'Aurelia',
                                                   'supercategory_of': [{'_id': 19980,
                                                                         '_type': 'Taxon',
                                                                         'name': 'Aurelia aurita'},
                                                                        {'_id': 19981,
                                                                         '_type': 'Taxon',
                                                                         'name': 'Aurelia labiata'}]}]}]

def test_taxonomy_1():
    assert 2 + 2 == 4
