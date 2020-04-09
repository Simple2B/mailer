from flask import Flask
from flask import request
from flask import jsonify
from invalid_usage import input_check, InvalidUsage
from work_mailer import Work_mailer
from format_mailer import Format_mailer


app = Flask(__name__, static_url_path='/static')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def index():
    raise NotImplementedError()


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/send_message', methods=['POST'])
def send_message():
    email = request.form['email']
    name = request.form['name']
    message = request.form['message']
    input_check(name, email, message)

    try:
        if not app.config['TESTING']:
            Work_mailer.send(email, name, message)
        else:
            Format_mailer.send(email, name, message)
    except: 

    return 'OK'
