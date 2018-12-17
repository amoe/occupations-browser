# Testing guide

A test utility function `occubrow.test_utility.make_backend` is available to
allow test writers to avoid configuring an entire Backend, which may have
several parts that can be mocked but normally would not be.  You pass the
Repository to this function, which it's your choice whether it be a mocked
repository or a non-mocked repository.

## Expecting calls on the backend

The current strategy is for the backend to take control over the submission of
queries, which are executed via the `run_statement` method on the repository.
Then it's possible to expect Cypher queries on the repository through the 
following method:

    def test_small_taxonomy_imports():
        mock_repository = Mock()
        runmock = mock_repository.run_statement
        backend = make_backend(mock_repository)
    
        # Call the system under test
        backend.import_taxonomy(input_data)

        calls = [
            call('CREATE (t:Taxon {content: $content})', content='Music'),
            call('CREATE (t:Taxon {content: $content})', content='Rock'),
            call('CREATE (t:Taxon {content: $content})', content='Classical'),

            call('MATCH (t1:Taxon {content: $start_node}), (t2:Taxon {content: $end_node})\n                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)', end_node='Rock', start_node='Music'),
            call('MATCH (t1:Taxon {content: $start_node}), (t2:Taxon {content: $end_node})\n                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)', end_node='Classical', start_node='Music')
        ]

        runmock.assert_has_calls(calls, any_order=True)

You can get the call list to store under `calls` by executing the
system-under-test and printing `mock.call_args_list`.  However you should be
writing it yourself.

Also, this method is quite ugly and fragile.  It would be better to formalize
the individual queries as discrete objects and test their properties, then have
another layer of tests asserting that they coerce to strings as expected.
