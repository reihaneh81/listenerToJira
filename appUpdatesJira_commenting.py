from atlassian import Jira
from pprint import pprint
import os
import json
from flask import request, make_response


def statusUpdatesByCommenting():

    jira = Jira(url='https://jira-test.nentgroup.com', username='reihaneh.vafaei@nentgroup.com', password='Renistrong&1025')
    print('Connection is Done Sucessfully to Jira')
    print('Here the approver name.family is storing into json file as approverInfo.json')
    dir = os.path.dirname(__file__)
    with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
        approverInfo = json.load(json_file)

    pprint(approverInfo)
    pprint(approverInfo['Approver'])
    Approver = approverInfo['Approver'][0]
    pprint(Approver)
    pprint(Approver['name'])

    issue_key = approverInfo['Issue_key'][0]
    pprint(issue_key)
    pprint(issue_key['name'])

    form_json = json.loads(request.form["payload"])

    print('it is')
    pprint(form_json)
    ts = form_json['message']
    print('this is time stamp', ts['ts'])
    selection = form_json["actions"][0]
    print(selection)
    pprint(selection)
    print(selection['text']['text'])

    userid = form_json['user']
    print('This is approvers name in Response', userid['name'])
    print('This is approvers username in Response', userid['username'])

    if userid['name'] == userid['username']:

        if selection['text']['text'] == "Approve":
            message_text_approve = "Approve"
            jira.issue_add_comment(issue_key['name'],
                                   ' This ticket is %sd in Slack by mailto:%s@nentgroup.com' % (message_text_approve,userid['username']))
        elif selection['text']['text'] == "Reject":
            message_text_reject = "Reject"
            jira.issue_add_comment(issue_key['name'],' This ticket is %sed in Slack by mailto:%s@nentgroup.com'%(message_text_reject,userid['username']))

    print('this commenting is done successfully')