// so the situation is
// We have two sources: 1 and 2
// These represent two four-word sentences:


// he jumped the fence
// Jake wanted the dog

CREATE
    (n1:Token {content: "he"}),
    (n2:Token {content: "jumped"}),
    (n3:Token {content: "the"}),
    (n4:Token {content: "fence"}),
    (n5:Token {content: "Jake"}),
    (n6:Token {content: "wanted"}),
    (n7:Token {content: "dog"}),
    (n8:Token {content: "neighbours"}),
    (n9:Token {content: "had"}),
    (n1)-[:PRECEDES {source: 1, index: 0}]->(n2),      
    (n2)-[:PRECEDES {source: 1, index: 1}]->(n3),      
    (n3)-[:PRECEDES {source: 1, index: 2}]->(n4),      
    (n3)-[:PRECEDES {source: 2, index: 3}]->(n7),      
    (n5)-[:PRECEDES {source: 2, index: 0}]->(n6),      
    (n6)-[:PRECEDES {source: 2, index: 1}]->(n3),
    (n7)-[:PRECEDES {source: 2, index: 2}]->(n3),
    (n3)-[:PRECEDES {source: 2, index: 4}]->(n8),
    (n8)-[:PRECEDES {source: 2, index: 5}]->(n9);



// This version only includes the index
    CREATE
        (t1:Token {content: "Jake"}),
        (t2:Token {content: "wanted"}),
        (det:Token {content: "the"}),
        (t3:Token {content: "dog"}),
        (t4:Token {content: "neighbours"}),
        (t5:Token {content: "had"}),
        (t1)-[:PRECEDES {index: 0}]->(t2),      
        (t2)-[:PRECEDES {index: 1}]->(det),      
        (det)-[:PRECEDES {index: 2}]->(t3),      
        (t3)-[:PRECEDES {index: 3}]->(det),      
        (det)-[:PRECEDES {index: 4}]->(t4),
        (t4)-[:PRECEDES {index: 5}]->(t5);


