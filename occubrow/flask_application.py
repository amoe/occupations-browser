import flask
import occubrow.system
from flask.json import jsonify
import pprint

app = flask.Flask("occubrow")

app.config['SERVER_NAME'] = 'localhost:5000'

backend = occubrow.system.get_backend()

cache = {
    '1': 'foo'
}

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
    depth_limit = int(flask.request.args.get('depth_limit'))
    taxon_uris = flask.request.args.getlist("filter[]")
    cooccurrence_threshold = int(flask.request.args.get('cooccurrence_threshold'))

    if taxon_uris:
        result = backend.search_with_taxons(token, taxon_uris, depth_limit, cooccurrence_threshold)
    else:
        result = backend.get_token_tree(token, depth_limit, cooccurrence_threshold)

    return jsonify(result)

@app.route('/contexts')
def get_contexts():
    token = flask.request.args.get('token')
    result = backend.get_contexts(token)
    return jsonify(result)

@app.route('/tokens')
def get_tokens():
    substring = flask.request.args.get('substring')
    if substring:
        result = backend.search_tokens(substring)
    else:
        result = backend.get_all_tokens()

    return jsonify(result)

@app.route('/centrality')
def get_centrality_statistics():
    return jsonify(backend.get_centrality_statistics())

@app.route('/micromacro-query', methods=['POST'])
def create_micromacro_query():
    # Flask will auto absolutize this.
    headers = {'Location': '/micromacro-query/1'}
    query_spec = flask.request.get_json()

    try:
        result = backend.query_micromacro(query_spec)
        cache['1'] = result
        return flask.Response(status=201, headers=headers)
    except occubrow.errors.CannotContactMicromacroError as e:
        return flask.Response(status=502)

@app.route('/micromacro-query/<identifier>', methods=['GET'])
def get_micromacro_query(identifier):
    return jsonify(cache[identifier])
