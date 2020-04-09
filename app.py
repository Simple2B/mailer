from flask import Flask
from flask import request
from flask import jsonify
from invalid_usage import input_check, InvalidUsage
from work_mailer import WorkMailer
from format_mailer import FormatMailer


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

    mailer = WorkMailer(email, name, message) if not app.config['TESTING'] else FormatMailer(email, name, message)
    mailer.send()

    return 'OK'
