import occubrow.types

def shim_node(node):
    labels = node.labels

    # Nodes should always have one and only one label under our data model
    if len(labels) != 1:
        raise Exception("node should have one label, corruption likely")

    # can't index into a frozenset so just pick an arbitrary one
    label = next(iter(labels))

    return occubrow.types.Node(
        node.id, label, dict(node.items())
    )

def shim_relationship(relationship):
    return occubrow.types.Relationship(
        relationship.start_node.id,
        relationship.end_node.id,
        dict(relationship.items()),
        relationship.type
    )


def shim_subgraph_result(row):
    return {
        'nodes': [shim_node(n) for n in row.value('nodes')],
        'rels': [shim_relationship(r) for r in row.value('rels')]
    }

