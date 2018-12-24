import flask

app = flask.Flask("occubrow")

@app.route('/')
def hello_world():
    return 'Hello, World!'
