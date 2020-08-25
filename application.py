from flask import Flask, request, redirect, url_for, jsonify
from flask_mail import Mail
from flask_mail import Message
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

application = Flask(__name__)

application.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'roboticsumass@gmail.com',
    MAIL_PASSWORD = 'wepno8-dagcim-qifjIk'
)

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

mail = Mail(app)
CORS(app)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@application.route("/contact/", methods=['POST'])
def submitButtonPushed_Contact():
    if request.method == 'POST':
        info = request.get_json()
        if 'firstName' in info and 'lastName' in info and 'subject' in info and 'email' in info and 'message' in info:
                msg = Message('[CONTACT] ' + info['subject'] + ' - ' +  info['email'] + ' (' + info['firstName'] + ' ' + info['lastName'] + ')', sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
                msg.body = info['message']
                mail.send(msg)
                return "Success", 200
    return "Record not found", 400


@application.route("/apply/", methods=['POST'])
def submitButtonPushed_Apply():
    if request.method == 'POST':
        info = request.get_json()
        if 'firstName' in info and 'lastName' in info and 'email' in info and 'major' in info and 'expGrad' in info and 'GorU' in info and 'qOne' in info and 'qTwo' in info and 'qThree' in info and 'qFour' in info and 'qFive' in info:
                msg = Message('APPLICATION ' + info['lastName'] + ' ' + info['lastName'] + ' - ' + info['email'], sender="roboticsumass@gmail.com", recipients=["roboticsumass@gmail.com"])
                msg.body = info['major'] + '\n\n' + info['expGrad'] + '\n\n' + info['GorU'] + '\n\n' + 'QUESTION 1:' + '\n\n' + info['qOne'] + '\n\n' + 'QUESTION 2:' + info['qTwo'] + '\n\n' + 'QUESTION 3:' + info['qThree'] + '\n\n' + 'QUESTION 4:' + info['qFour'] + '\n\n' + 'QUESTION 5:' + info['qFive']
                mail.send(msg)

                msg = Message('Application Received!', sender="roboticsumass@gmail.com", recipients=[info['email']])
                msg.body = 'We have received your application ' + info['firstName'] + '! Should you be a good fit for our team we will be sure to reach out to you for an interview! We will try to get back to you within the coming month but this may change so please be patient! Thank you!'
                mail.send(msg)
                return "Success", 200
    return "Record not found", 400

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS