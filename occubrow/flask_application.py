import flask
import occubrow.system
from flask.json import jsonify

app = flask.Flask("occubrow")
backend = occubrow.system.get_backend()

@app.route('/tree')
def get_tree():
    root = flask.request.args.get('root')
    return jsonify(backend.get_token_tree(root))

@app.route('/taxonomy')
def get_taxonomy():
    root = flask.request.args.get('root')
    return jsonify(backend.export_taxonomy_tree(root))
