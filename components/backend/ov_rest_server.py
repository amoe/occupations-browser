import flask
import flask.logging
import graph_operations
import graph_operations_tezra
import logging
import neo4j_repository

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
    app.neo4j = neo4j_repository.Neo4jRepository(port=7688)

    return app

app = create_app()

@app.route('/my-endpoint', methods=['GET'])
def get_corpus():
    return flask.jsonify({'foo': 42})

@app.route('/tree', methods=['GET'])
def get_tree_by_root():
    root = flask.request.args.get('root')
    return flask.jsonify(graph_operations.get_tree_by_root(root))

@app.route('/delete_some_node', methods=['POST'])
def delete_some_node():
    graph_operations.delete_node('fox');
    return ('', 204);


@app.route('/clear_all_nodes', methods=['POST'])
def clear_all_nodes():
    graph_operations.clear_entire_graph()
    return ('', 204);


@app.route('/all_roots', methods=['GET'])
def get_all_roots():
    return flask.jsonify(graph_operations.get_all_roots())

@app.route('/tezra/tree', methods=['GET'])
def tezra_get_tree():
    root = flask.request.args.get('root')
    zoom_depth = int(flask.request.args.get('zoom_depth'))
    return flask.jsonify(graph_operations_tezra.get_tree_by_root(root, zoom_depth))

@app.route('/tezra/roots', methods=['GET'])
def tezra_get_roots():
    q = flask.request.args.get('q')
    result = flask.current_app.neo4j.get_roots_with_substring_match(q)
    return flask.jsonify(result)

# what does it mean to ask for the source?
# We can only ask for a source by node.
@app.route('/tezra/sources', methods=['GET'])
def tezra_get_sources():
    # Sources should return a list of sentence identifiers.
    sources = [
        {'token_list': ["the", "quick", "brown", "fox"],
         'source': 1},
        {'token_list': ["jake", "had", "a", "dog"],
         'source': 2}
    ]
    return flask.jsonify(sources)
    
