# Neo4j-Python-Driver: The Missing Manual

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
