CONSTRAINTS = [
    "CREATE CONSTRAINT ON (to:Token) ASSERT to.content IS UNIQUE",
    "CREATE CONSTRAINT ON (s:Sentence) ASSERT s.uuid IS UNIQUE",
    "CREATE CONSTRAINT ON (ta:Taxon) ASSERT ta.uri IS UNIQUE"
]

INDEXES = [
    "CREATE INDEX ON :Taxon(key)"
]

def create_constraints(driver):
    print("Creating constraints.")
    with driver.session() as session:
        for constraint_stmt in CONSTRAINTS:
            session.run(constraint_stmt)
    print("Created constraints.")

def create_indexes(driver):
    print("Creating constraints.")
    with driver.session() as session:
        for index_stmt in INDEXES:
            session.run(index_stmt)
    print("Created constraints.")


def reset_schema(driver):
    drop_calls = []

    with driver.session() as session:
        r = session.run("CALL db.constraints");
        for r2 in r:
            index_desc = r2.value('description')
            drop_calls.append("DROP %s" % index_desc)

        for drop_call in drop_calls:
            session.run(drop_call)

    drop_calls = []

    # we have to get a new session between these two so that the change
    # can be committed

    with driver.session() as session:
        r = session.run("CALL db.indexes");
        for r2 in r:
            index_desc = r2.value('description')
            drop_calls.append("DROP %s" % index_desc)
