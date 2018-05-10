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




