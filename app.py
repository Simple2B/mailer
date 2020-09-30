from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from invalid_usage import input_check, InvalidUsage
from simplebot import SimpleBot
from logger import log
from flask import render_template
from settings import Settings
from ses import send_email
import datetime


app = Flask(__name__, static_url_path="/static")


app.config["MAIL_SERVER"] = 'email-smtp.us-east-2.amazonaws.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = 'AKIARBQLSALCZLH36JLT'
app.config["MAIL_PASSWORD"] = 'BC1KRf/k17AShl7uNfN2Lb4a4Nc75jWjj01TdxqqgGsK'
app.config["MAIL_USE_TLS"] = True

CORS(app)
log.set_level(log.DEBUG)
log(log.DEBUG, "start server")


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send_message", methods=["POST"])
def send_message():
    log(log.DEBUG, "/send_message")
    email = request.form["email"]
    name = request.form["name"]
    message = request.form["message"]
    flaattachment = request.files["file"] if "file" in request.files else None
    input_check(name, email, message)
    log(log.INFO, "got message from:%s(%s)", name, email)
    day = datetime.datetime.today()

    data = {
            "name": name,
            "email": email,
            "message": message,
            "day": day.strftime("%A, %B %d"),
            "year": day.strftime("%Y")
        }

    cfg = Settings()

    send_email(app, data, flaattachment)

    if "telegram" in cfg.conf:
        # send notification to telegram channel
        # if not app.config["TESTING"]:
        bot = SimpleBot()
        bot.send(name=name)
    else:
        log(log.INFO, "telegram bot not configured")

    return "OK"
