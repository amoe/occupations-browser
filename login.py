import neo4j

user = "neo4j"
password = "password"
auth_token = (user, password)
driver = neo4j.GraphDatabase.driver("bolt://localhost:15734", auth=auth_token)
