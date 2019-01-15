set -e


clear_n4j() {
    # Note that cypher-shell is buggy and does not support the pipe properly
    # so we have to pass on the command line
    qry='MATCH (n) DETACH DELETE n'
    cypher-shell -a bolt://localhost:7688 -u neo4j -p password "$qry"
}    


clear_n4j
python3 attempt_samuels_load.py ~/download/media_405073_en.xlsx
python3 scripts/format_samuels_ob_data.py ~/dev/samdist/intermediate_data/m_nonl_combined.csv
python3 import_sample_sentences.py samuels-annotated.xml

