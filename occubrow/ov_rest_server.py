import flask
import flask.logging
import logging
import occubrow.neo4j_repository

def create_app():
    # Enable this to get logging output
    #logging.basicConfig(level=logging.DEBUG)

    app = flask.Flask(__name__)
    for logger in (
        app.logger,
        logging.getLogger('occubrow'),
    ):
        logger.addHandler(flask.logging.default_handler)


    # Should come from config
    app.neo4j = occubrow.neo4j_repository.Neo4jRepository(port=7688)

    return app

app = create_app()

@app.route('/tezra/tree', methods=['GET'])
def tezra_get_tree():
    root = flask.request.args.get('root')
    zoom_depth = int(flask.request.args.get('zoom_depth'))
    return flask.jsonify(flask.current_app.neo4j.get_tree_by_root(root, zoom_depth))

@app.route('/tezra/roots', methods=['GET'])
def tezra_get_roots():
    q = flask.request.args.get('q')
    result = flask.current_app.neo4j.get_roots_with_substring_match(q)
    return flask.jsonify(result)
