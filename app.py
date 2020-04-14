from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from invalid_usage import input_check, InvalidUsage
from work_mailer import WorkMailer
from format_mailer import FormatMailer
from simplebot import SimpleBot
from logger import log

app = Flask(__name__, static_url_path='/static')
CORS(app)
log.set_level(log.DEBUG)
log(log.DEBUG, 'start server')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def index():
    return 'mailer'


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/send_message', methods=['POST'])
def send_message():
    log(log.DEBUG, '/send_message')
    email = request.form['email']
    name = request.form['name']
    message = request.form['message']
    input_check(name, email, message)
    log(log.INFO, 'got message from:%s(%s)', name, email)

    # sent e-mail
    mailer = WorkMailer(email, name, message) if not app.config['TESTING'] else FormatMailer(email, name, message)
    mailer.send()
    # send notification to telegram channel
    if not app.config['TESTING']:
        bot = SimpleBot()
        bot.send(name=name)

    return 'OK'
