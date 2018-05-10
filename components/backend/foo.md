Given the following graph:



Which is creatable by the following Cypher script:

    CREATE
        (n1:Token {content: "lonely"}),
        (n2:Token {content: "island"}),
        (n1)-[:PRECEDES]->(n2);


    CREATE
        (n1:Token {content: "the"}),
        (n2:Token {content: "quick"}),
        (n3:Token {content: "brown"}),
        (n4:Token {content: "fox"}),
        (n5:Token {content: "bear"}),
        (n1)-[:PRECEDES]->(n2),
        (n2)-[:PRECEDES]->(n3),
        (n3)-[:PRECEDES]->(n4),
        (n3)-[:PRECEDES]->(n5);

I want a query that will return nodes in the path from a given root, following
the PRECEDES relationships backwards.  The query should *also* return all
incoming relationships for the given node, so that I can construct the subgraph
in-memory later.  However, the list of incoming relationships should never point
outside of the returned root.

For instance, if I query for the root `lonely`, I want the result:

    +-----------------------------------------------------------------------+
    | (:Token {content: "lonely"}) | []                                     |
    | (:Token {content: "island"}) | [[:PRECEDES]]                          |
    +-----------------------------------------------------------------------+

If I query for the root `the`, I want the result:

    +-----------------------------------------------------------------------+
    | (:Token {content: "the"})   | []                                      |
    | (:Token {content: "quick"}) | [[:PRECEDES]]                           |
    | (:Token {content: "brown"}) | [[:PRECEDES]]                           |
    | (:Token {content: "fox"})   | [[:PRECEDES]]                           |
    | (:Token {content: "bear"})  | [[:PRECEDES]]                           |
    +-----------------------------------------------------------------------+

If I query for the root `brown`, I want the following result, note that the
incoming relationship for `brown` itself has been elided because it would
point outside of the subgraph.

    +-----------------------------------------------------------------------+
    | (:Token {content: "brown"}) | []                                      |
    | (:Token {content: "fox"})   | [[:PRECEDES]]                           |
    | (:Token {content: "bear"})  | [[:PRECEDES]]                           |
    +-----------------------------------------------------------------------+

The root and leaf nodes should always be included in the result.

This is my attempt so far:

    MATCH (a:Token {content: {root}})-[:PRECEDES*]->(t:Token)
    WITH COLLECT(a) + COLLECT(DISTINCT t) AS nodes_
    UNWIND nodes_ AS n
    OPTIONAL MATCH p = (n)-[r]-()
    WITH n AS n2, COLLECT(DISTINCT RELATIONSHIPS(p)) AS nestedrel
    RETURN n2, REDUCE(output = [], rel in nestedrel | output + rel) AS rels

This is sort-of close but has several problems: the use of `COLLECT(a)` to
artificially include the root is kind of hacky, it leaves relationships that
point away from the root in the relationship result, and if you try to use a
leaf node as the root it won't return any nodes at all.  (The `REDUCE` part is
just flattening the relationship list by one level.)

[FYI the application is I need to rebuild this tree structure in memory as a
NetworkX MultiDiGraph.]
