import flask
import graph_operations
import graph_operations_tezra

def create_app():
    app = flask.Flask(__name__)
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
    return flask.jsonify(graph_operations_tezra.get_tree_by_root(root))

@app.route('/tezra/roots', methods=['GET'])
def tezra_get_roots():
    q = flask.request.args.get('q')
    return flask.jsonify(graph_operations_tezra.get_roots_with_substring_match(q))
