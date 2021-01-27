from flask_mail import Mail, Message
from flask import render_template


def send_email(app, data, subject, att, cfg):
    mail = Mail(app)
    msg = Message(subject=subject,
                  sender=cfg.conf["ses"]["SENDER"],
                  recipients=[cfg.conf["ses"]["RECEIVER"], ])
    msg.html = render_template("contact_email.html", data=data)
    if att:
        msg.attach(att.filename, att.content_type, att.read())
    mail.send(msg)
