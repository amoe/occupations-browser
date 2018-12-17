# Neo4j-Python-Driver: The Missing Manual

## Manually handling session open and close

The definition of the context handler is just as such:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


So you can just make sure that you call close afterward

## Finding the results summary of an executed statement

.summary() object on a BoltStatementResult will give a
BoltStatementResultSummary object.  You can get execution plans.  You can get
.counters attribute. This is going to give a SummaryCOunters object.  Don't try
to print it, just access attributes on it.

SummaryCounters has data attached to it that gets updated, eg

    nodes_created = 0
    nodes_deleted = 0
    relationships_created = 0
    relationships_deleted = 0
    properties_set = 0
    labels_added = 0
    labels_removed = 0
    indexes_added = 0
    indexes_removed = 0
    constraints_added = 0
    constraints_removed = 0


## Adding arbitrary properties to a node when it's created

    def run(self, statement, parameters=None, **kwparameters):
    tx.run("CREATE (t:Taxon $props)", props={'name': 'Dave', 'age': 42}).summary()

## BoltStatementResult

## `read_transaction(unit_of_work)`

This will establish a transaction and `unit_of_work` (a function) will be applied
with the arguments `tx` (a transaction handle).  Any remaining arguments will be
passed to `unit_of_work`.

    def print_friends(tx, name):
        for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) "
                             "WHERE a.name = {name} "
                             "RETURN friend.name", name=name):
            print(record["friend.name"])

    session.read_transaction(print_friends, "Alice")

## Relationship objects

Have the property 'start_node' and 'end_node'

## Node objects

Have an attribute `.labels ` that returns the labels of the node, and note there
can be more than one label.  This is returned as a frozenset.
