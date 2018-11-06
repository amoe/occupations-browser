import neo4j
import boltkit.controller
import boltkit.config

home = "ext/neo4j-community-3.4.6"

bolt_uri = "bolt://localhost:15374"

user = "neo4j"
password = "password"
auth_token = (user, password)


realpath = boltkit.controller._install(
    edition='community',
    version='3.4.6',
    path="ext"
)


controller = boltkit.controller.UnixController(home=realpath, verbosity=0)
controller.start()
controller.create_user(user, password)
controller.set_user_role(user, "admin")

driver = neo4j.GraphDatabase.driver(bolt_uri, auth=auth_token)
controller.stop()
