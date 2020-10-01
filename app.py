import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask_cors import CORS
from invalid_usage import input_check, InvalidUsage
from simplebot import SimpleBot
from settings import Settings
from ses import send_email
from logger import log


app = Flask(__name__, static_url_path="/static")

cfg = Settings()

app.config["MAIL_SERVER"] = cfg.conf["ses"]["MAIL_SERVER"]
app.config["MAIL_PORT"] = cfg.conf["ses"]["MAIL_PORT"]
app.config["MAIL_USERNAME"] = cfg.conf["ses"]["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = cfg.conf["ses"]["MAIL_PASSWORD"]
app.config["MAIL_USE_TLS"] = cfg.conf["ses"]["MAIL_USE_TLS"]


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
    attachment = request.files["file"] if "file" in request.files else None
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

    send_email(app, data, f"Message from: {name}", attachment, cfg)

    if "telegram" in cfg.conf:
        # send notification to telegram channel
        # if not app.config["TESTING"]:
        bot = SimpleBot()
        bot.send(name=name)
    else:
        log(log.INFO, "telegram bot not configured")

    return "OK"
