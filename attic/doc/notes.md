2018-11-05

USING PERIODIC COMMIT
LOAD CSV FROM 'https://neo4j.com/docs/developer-manual/3.4/csv/artists.csv' AS line
CREATE (:Artist { name: line[1], year: toInteger(line[2])})
