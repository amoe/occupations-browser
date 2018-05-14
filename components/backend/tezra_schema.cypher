// tezra schema

CREATE
  (s1:Sentence {tokens: ["Jake", "wanted", "the", "dog", "the", "neighbours", "had"]}),
  (t1:Token {content: "Jake"}),
  (t2:Token {content: "wanted"}),
  (det:Token {content: "the"}),
  (t3:Token {content: "dog"}),
  (t4:Token {content: "neighbours"}),
  (t5:Token {content: "had"}),
  (s1)-[:CONTAINS {index: 0, firstToken: true}]->(t1),
  (s1)-[:CONTAINS {index: 1}]->(t2),
  (s1)-[:CONTAINS {index: 2}]->(det),
  (s1)-[:CONTAINS {index: 3}]->(t3),
  (s1)-[:CONTAINS {index: 4}]->(det),
  (s1)-[:CONTAINS {index: 5}]->(t4),
  (s1)-[:CONTAINS {index: 6, lastToken: true}]->(t5);

MATCH (s1:Sentence)-[r:CONTAINS]->(t1:Token)
RETURN t1, r.index
ORDER BY r.index;

