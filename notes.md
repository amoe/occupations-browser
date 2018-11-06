2018-11-06

    # names = set()
    # print = names.add

    # def print_friends(tx, name):
    #     for record in tx.run("MATCH (a:Person)-[:KNOWS]->(friend) "
    #                          "WHERE a.name = {name} "
    #                          "RETURN friend.name", name=name):
    #         print(record["friend.name"])

    # with driver.session() as session:
    #     session.run("MATCH (a) DETACH DELETE a")
    #     session.run("CREATE (a:Person {name:'Alice'})-[:KNOWS]->({name:'Bob'})")
    #     session.read_transaction(print_friends, "Alice")

    # assert len(names) == 1
    # assert "Bob" in names


2018-11-05

"Protocol family unavailable" on travis -- 

I ran into this in the process of setting up travis-ci; within its environments,
ipv6 :: is resolved, but cannot be bound. Fixed by 36c77dd.

Need to re-derive the integration test base case and reform it as neo4j.
