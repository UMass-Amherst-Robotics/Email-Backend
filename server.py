from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_mail import Message
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import re

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


@app.route('/donators/', methods=['GET'])
def donators():
    with open('./donators.json', 'r') as file:
        donators = json.load(file)
        return donators


def getDonators():
    options = Options()
    options.add_argument('--headless')

    PATH = '/home/andrewtran47/Robotics/GFM/chromedriver'

    browser = webdriver.Chrome(PATH, options=options)

    browser.get("https://www.gofundme.com/f/umass-robotics/donations")

    # find list items
    items = browser.find_elements_by_class_name('o-donation-list-item')

    donations = [item.text for item in items]

    # get name and donation amount from the item and put into a set_trace if not anonymous
    donations = [donator.split('\n')[0:2] for donator in donations if donator.split('\n')[0] != 'Anonymous ']

    # removes unwanted stuff
    donations = [donation for donation in donations if not donation[0].startswith('Join this list') if not donation == ['']]

    # remove white space at end of every name and $
    for donation in donations:
        donation[0] = donation[0][:-1].title()
        donation[1] = int(donation[1].strip().replace('$',''))
        if 'And' or 'and' in donation[0]:
            donation[0] = re.sub('And|and', '&', donation[0])

    donator_info = []

    # give donation level for each donator
    for donation in donations:
        name, val = donation

        lvl = False

        if val >= 100:
            lvl = 'Gold'
        elif 50 <= val < 100:
            lvl = 'Silver'
        elif 25 <= val < 50:
            lvl = 'Base'

        donator_info.append((name, val, lvl))

    # only donators who paid > 25
    disp_donators = [donator for donator in donator_info if donator_info[2] is not False]

    # get rid of repeats
    closed = []
    for donator in disp_donators:
        replaced = False
        for i, val in enumerate(closed):
            if donator[0] == val[0]:
                if donator[1] > val[1]:
                    closed[i] = donator
                    replaced = True
        if replaced is False:
            closed.append(donator)

    # add gold/silver donator to list
    donators = {'gold':[], 'silver':[]}
    for donator in closed:
        if donator[2] == 'Gold':
            donators['gold'].append(donator[0])
        if donator[2] == 'Silver':
            donators['silver'].append(donator[0])

    with open('donators.json', 'w') as file:
        json.dump(donators, file)
