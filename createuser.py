import boltkit.controller

home = "ext/neo4j-community-3.4.6"

user = "neo4j"
password = "password"
auth_token = (user, password)


ctrl = boltkit.controller.UnixController(home=home)

