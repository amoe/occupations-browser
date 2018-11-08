# Neo4j-Python-Driver: The Missing Manual

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
can be more than one label.
