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
        if 'fName' in info and 'lName' in info and 'email' in info and 'qOne' in info and 'qTwo' in info and 'qThree' in info and 'qFour' in info and 'qFive' in info:
            msg = Message('[APPLICATION] ' + info['fName'] + ' ' + info['lName'], sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
            msg.body = 'QUESTION 1:' + ' ' + info['qOne'] + '\nQUESTION 2:' + info['qTwo'] + '\nQUESTION 3:' + info['qThree'] + '\nQUESTION 4:' + info['qFour'] + '\nQUESTION 5:' + info['qFive']
            mail.send(msg)
            return "Success", 200
    return "Record not found", 400
