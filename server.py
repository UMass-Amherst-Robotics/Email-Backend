from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_mail import Message
from flask_cors import CORS

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'roboticsumass@gmail.com',
    MAIL_PASSWORD = 'wepno8-dagcim-qifjIk'
)

mail = Mail(app)
CORS(app)

@app.route("/contact/", methods=['POST'])
def submitButtonPushed_Contact():
    if request.method == 'POST':
        info = request.get_json()
        if 'firstName' in info and 'lastName' in info and 'subject' in info and 'email' in info and 'message' in info:
                msg = Message('[CONTACT] ' + info['subject'] + ' - ' +  info['email'] + ' (' + info['firstName'] + ' ' + info['lastName'] + ')', sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
                msg.body = info['message']
                mail.send(msg)
                return "Success", 200
    return "Record not found", 400


@app.route("/apply/", methods=['POST'])
def submitButtonPushed_Apply():
    if request.method == 'POST':
        info = request.get_json()
        if 'firstName' in info and 'lastName' in info and 'email' in info and 'qOne' in info and 'qTwo' in info and 'qThree' in info and 'qFour' in info and 'qFive' in info:
                msg = Message('APPLICATION ' + info['firstName'] + ' ' + info['lastName'] + ' - ' + info['email'], sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
                msg.body = 'QUESTION 1:' + ' ' + info['qOne'] + 'QUESTION 2:' + info['qTwo'] + 'QUESTION 3:' + info['qThree'] + 'QUESTION 4:' + info['qFour'] + 'QUESTION 5:' + info['q5']
                mail.send(msg)

                msg = Message('Application Received!', sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
                msg.body = 'We have received your application ' + info['firstName'] + '! Should you be a good fit for our team we will be sure to reach out to you for an interview! We will try to get back to you within the coming month but this may change so please be patient! Thank you!'
                mail.send(msg)
                return "Success", 200
    return "Record not found", 400
