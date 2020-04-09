from flask import Flask, url_for
from flask import request
from flask import jsonify
from invalid_usage import InvalidUsage
import re
from const import MAX_NAME_LEN, MAX_MESSAGE_LEN
import smtplib
from my_secur import MY_MAIL, MY_PASSW

app = Flask(__name__, static_url_path='/static')


def input_check(name, email, message):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(regex,email) is None:
        return 'invalid email'
    if len(message) > MAX_MESSAGE_LEN:
        return 'long message'
    if len(name) > MAX_NAME_LEN:
        return 'long name'
    return None


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
        error = input_check(name, email, message)
        if error:
            raise InvalidUsage(error, status_code=410)
        
        message_to_send = 'HI, {} we\'re glad you have such a good idea. '.format(name)
        server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
        server.starttls() # Use TLS
        server.login(MY_MAIL, MY_PASSW) # Login to the email server
        server.sendmail(MY_MAIL, email , message_to_send) # Send the email
        server.quit() # Logout of the email server
        return 'OK POST'
    else:
        return 'OK GET'
