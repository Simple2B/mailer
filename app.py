from flask import Flask
from flask import request
from flask import jsonify
from invalid_usage import input_check, InvalidUsage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
from my_secur import MY_MAIL, MY_PASSW


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

    if not app.config['TESTING']:
        # mail_text = "HI, {name} we're glad you have such a good idea. "
        # message_to_send = mail_text.format(name=name)

        msg = MIMEMultipart()
        msg['From'] = 'email'
        msg['To'] = 'send_to_email'
        msg['Subject'] = 'subject'
        msg.attach(MIMEText(message, 'plain'))
        message_to_send = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)  # Connect to the server
        server.starttls()  # Use TLS
        server.login(MY_MAIL, MY_PASSW)  # Login to the email server
        server.sendmail(MY_MAIL, email, message_to_send)  # Send the email
        server.quit()  # Logout of the email server
    return 'OK'
