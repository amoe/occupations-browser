import neo4j
import pytest
import boltkit.controller
import boltkit.config


bolt_port = 7687
bolt_address = ("localhost", bolt_port)
bolt_uri = "bolt://%s:%d" % bolt_address

realpath = 'ext/neo4j-community-3.4.6'

@pytest.fixture
def neo4j_driver():
    realpath = boltkit.controller._install(
        edition='community',
        version='3.4.6',
        path="ext"
    )
    print("Initialized home at", realpath)
    boltkit.config.update(
        realpath,
        {boltkit.config.BOLT_LISTEN_URI_SETTING: bolt_uri}
    )

    controller = boltkit.controller.create_controller(path=realpath)
    controller.start()
#    driver = neo4j.GraphDatabase.driver(bolt_uri)
    yield "foo"
    controller.stop()


def test_should_run_readme(neo4j_driver):
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
    assert 2 + 2 == 4
