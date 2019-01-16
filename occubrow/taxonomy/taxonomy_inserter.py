import neo4j

# loads a taxonomy where expected format has unique uri as the node value
# and contains attribute 'content' giving the human-readable name

class TaxonomyInserter(object):
    def __init__(self, driver):
        self.driver = driver

    def load_taxonomy(self, g):
        with self.driver.session() as s:
            self.do_insert(s, g)

    def do_insert(self, s, g):
        for uri, data in g.nodes(data=True):
            print(uri, data)
            params = {'uri': uri, 'content': data['content']}
            s.run("CREATE (t:Taxon {uri: {uri}, content: {content}})", params)

        for u_uri, v_uri in g.edges:
            s.run("""
                MATCH (t1:Taxon {uri: {u_uri}}), (t2:Taxon {uri: {v_uri}})
                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)
            """, {'u_uri': u_uri, 'v_uri': v_uri})
            

