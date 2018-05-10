import flask
import graph_operations

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
