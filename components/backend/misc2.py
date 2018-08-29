# does a dfs and removes ids from a tree

# NB: no longer used, was only needed to try to work around some networkx stuff
# deep-compare doesn't work for trees anyway because child nodes can come
# out in an arbitrary ordering

def visit(node):
    print("Visiting node: id was %d" % node['id'])
    del node['id']

def strip_ids(tree):
    visited = set()
    to_visit = [tree]

    while to_visit:
        node = to_visit.pop()

        if node['id'] not in visited:
            # order is important here
            visited.add(node['id'])
            visit(node)
            for child in node.get('children', []):
                if child['id'] not in visited:
                    to_visit.append(child)

