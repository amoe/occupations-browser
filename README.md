# occupations-browser

## Install front end dependencies

    $ make gather_dependencies

This needs Yarn to work.

## Back end dependencies

Notably: networkx (latest in pip), nltk (punkt tokenizer), neo4j (1.7+), flask (latest in pip)

## Running

Run the backend:

    amoe@cslp019129 $ make run_backend

Run the frontend:

    amoe@cslp019129 $ make run_frontend

These will both run in auto-reloading modes so that you can make changes to the
code.

## Connect to a Cypher shell

    cypher-shell -a localhost:7688

If you get connection refused, you need to actually start neo4j.  `systemctl
start neo4j`.

## Deployment

OCCUBROW requires a Neo4j server present on the host system.
The neo4j server is expected to ru on port 7688 for Bolt connections.

### Load the data

Run the Python script `scripts/import_data.py` to load the data.

    python3 scripts/import_data.py sample.csv

This will import the sample data.  You should now be able to view the sample
data token graph by logging into the Neo4j browser at localhost:7475.

### Deploy the Flask server code

This requires Fabric 2.2.1+.

Yow! x4
