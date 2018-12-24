import flask
import occubrow.system
from flask.json import jsonify

app = flask.Flask("occubrow")
backend = occubrow.system.get_backend()



@app.route('/tree')
def get_tree():
    root = flask.request.args.get('root')
    return jsonify(backend.get_tree(root))
