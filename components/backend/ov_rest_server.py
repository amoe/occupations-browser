import flask

def create_app():
    app = flask.Flask(__name__)
    return app

app = create_app()

@app.route('/my-endpoint', methods=['GET'])
def get_corpus():
    return flask.jsonify({'foo': 42})
