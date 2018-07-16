#! /bin/sh

qry1="MATCH (n) RETURN COUNT (n);"
qry2="MATCH (n) DETACH DELETE n;"

printf "%s" "$qry1" | cypher-shell -u neo4j -p password
printf "%s" "$qry2" | cypher-shell -u neo4j -p password
printf "%s" "$qry1" | cypher-shell -u neo4j -p password
