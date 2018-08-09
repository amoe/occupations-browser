# occupations-browser

## Running

Run the backend:

    amoe@cslp019129 $ make run_backend

Run the frontend:

    amoe@cslp019129 $ make run_frontend

These will both run in auto-reloading modes so that you can make changes to the
code.

## Connect to a Cypher shell

    cypher-shell -u neo4j -p password

If you get connection refused, you need to actually start neo4j.  `systemctl start neo4j`.

## Deployment

OCCUBROW requires a Neo4j server present on the host system.
The neo4j server is expected to ru on port 7688 for Bolt connections.

### Load the data

Run the Python script `scripts/import_data.py` to load the data.

    python3 scripts/import_data.py data/1-obo1674-1834_occupations_20180104.csv

Yow! x2
