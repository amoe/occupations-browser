# Tree Model JS -- the missing manual

## Determine level of a given node

node.getPath()

## Get all nodes at a given level

Should be the following:

    root.all(n => n.getPath().length == 1)

A path of length 1 is only present for the root node.

## Access node data

All data in the tree is present in the `.model` sub-object of the node object.

So to convert a node to its string value, you should try:

    myNodesList.map(n => n.model.content)

Remember this is extremely non-typesafe.
