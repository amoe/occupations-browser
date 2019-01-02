import neo4j

class TaxonomyInserter(object):
    def __init__(self, driver):
        self.driver = driver

    def load_taxonomy(self, g):
        self.index = {}
        with self.driver.session() as s:
            self.do_insert(s, g)

    def make_tag_uri(self, s):
        candidate_found = False
        n = 1
        candidate = None

        while not candidate_found:
            candidate = "tag:solasistim.net,2018-12-28:occubrow/%s/%d" % (s, n)
            if candidate in self.index:
                n += 1
                continue
            else:
                self.index[candidate] = s
                candidate_found = True

        return candidate

    def lookup(self, n):
        inverted_dict = {v: k for k, v in self.index.items()}
        return inverted_dict[n]
        
    def do_insert(self, s, g):
        for n in g.nodes:
            uri = self.make_tag_uri(n)
            params = {'uri': uri, 'content': n}
            s.run("CREATE (t:Taxon {uri: {uri}, content: {content}})", params)

        for u, v in g.edges:
            u_uri = self.lookup(u)
            v_uri = self.lookup(v)

            s.run("""
                MATCH (t1:Taxon {uri: {u_uri}}), (t2:Taxon {uri: {v_uri}})
                CREATE (t1)-[:SUPERCATEGORY_OF]->(t2)
            """, {'u_uri': u_uri, 'v_uri': v_uri})
            

