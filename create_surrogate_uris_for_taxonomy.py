import networkx

# expects a graph with only string nodes and edges
# the string node represents the value for content
# we should be returning a new graph with the string value moved into an attribute

class TaxonomySurrogateURIAssigner(object):
    def assign(self, g):
        self.index = {}
        
        g2 = networkx.DiGraph()

        for n in g.nodes:
            uri = self.make_tag_uri(n)
            g2.add_node(uri, content=n)

        for u, v in g.edges:
            u_uri = self.lookup(u)
            v_uri = self.lookup(v)
            g2.add_edge(u_uri, v_uri)
        
        return g2

    def lookup(self, n):
        inverted_dict = {v: k for k, v in self.index.items()}
        return inverted_dict[n]

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
        
