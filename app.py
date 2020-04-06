from flask import Flask, url_for
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return app.send_static_file('favicon.ico')
