from flask import Flask, url_for
from flask import request
from flask import jsonify
from invalid_usage import InvalidUsage
import re

app = Flask(__name__, static_url_path='/static')


def input_check(name, mail, message):

    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
    mail_check = re.search(regex,email
    name_check = len(name) > 50
    message_check = len(message) > 1000
    pass
    return name_check and mail_check and message_check

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/send_message', methods=['GET', 'POST'])  #TODO: remove 'GET'
def send_message():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        message = request.form['message']
        a = input_chek(name, mail, message)
           # raise InvalidUsage('Invalide name', status_code=410)

        return 'OK POST'
    else:
        return 'OK GET'
