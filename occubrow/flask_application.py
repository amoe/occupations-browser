import flask
import occubrow.system
from flask.json import jsonify

app = flask.Flask("occubrow")
backend = occubrow.system.get_backend()

@app.route('/tree')
def get_tree():
    root = flask.request.args.get('root')
    depth_limit = flask.request.args.get('depth_limit')

    return jsonify(backend.get_token_tree(root, int(depth_limit)))

@app.route('/taxonomy')
def get_taxonomy():
    root = flask.request.args.get('root')
    return jsonify(backend.export_taxonomy_tree(root))

@app.route('/metrics')
def get_metrics():
    return jsonify(backend.get_metrics())

@app.route('/random-root')
def get_random_root():
    return jsonify(backend.pick_root())

@app.route('/taxonomy-roots')
def get_taxonomy_roots():
    return jsonify(backend.get_taxonomy_roots())
                   

@app.route('/query')
def get_token_query():
    # this is the format that axios uses
    token = flask.request.args.get('root')
    taxon_uris = flask.request.args.getlist("filter[]")
    result = backend.search_with_taxon(token, taxon_uris)
    print(result)
    return jsonify(result)
