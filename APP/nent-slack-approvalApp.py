from flask import Flask
from flask import json
from flask import request, make_response,Response
import os
#from appSendMessageToslack import AppToSlack
#import appUpdatesJira_commenting
#import slack
import re
from pprint import pprint
from atlassian import Jira
from flask import json
from flask import request, make_response
import slack
import time
import os
from pprint import pprint


"""This is name Of Application 
   The one we are going to listen
"""
app1 = Flask(__name__)

"""
     This is route of App as a simple example which display the message on web when we run app it
"""


# Our app's Slack Event Adapter for receiving actions via the Events API
#slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_signing_secret="3c2d1de5482fb85642d214cf5693b0c1"

#SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]
SLACK_VERIFICATION_TOKEN="sCwtOSXiaWrU4eoSYVgRS9Hg"
# Create a SlackClient for your bot to use for Web API requests
#slack_bot_token = os.environ["App_Token"]

slack_bot_token='xoxb-577663161824-1224571947153-QpntoV11hM4H8nhNg9tlX05t'
slack_client = slack.WebClient(slack_bot_token)

#AppToSlack = AppToSlack()

# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)


@app1.route('/')
def api_root():

    return('Welcome To return')

"""
    to post data to app which is coming from Jira , to that I set up the webhook url by using ngrok/webhook , 
    which allows to post data in real time when the new Jira ticket is created and we can sort of split 
    which kinds of information we need to  receive such as IssueTyoe, Summary/description, Reporter name and 
    the main part Approval name.family
"""
@app1.route('/webhook', methods=['POST'])
def api_jiraTest_message():


                 data = request.get_json()
                 #pprint(data)

                 print('To Retrieve All Created Ticket info')

                 """
                 To Fetch Reporter name
                 """
                 Reporter = data['issue']['fields']['reporter']
                 #print('All the information about Reporter')
                 #pprint(Reporter)
                 Reporter_name = Reporter['name']
                 print('this is print reporter name')
                 pprint(Reporter_name)

                 """
                 Its splits @sign + domain  email
                 """
                 regexStr = r'^([^@]+)@[^@]+$'
                 emailStr = Reporter['name']
                 Reporter = re.search(regexStr, emailStr)
                 if not Reporter is None:
                     print('print name and familyname of reporter', Reporter.group(1))
                 else:
                     print("Did not match")

                 """
                 To Fetch Issue Type
                 """
                 Issue_Type = data['issue']['fields']['issuetype']['name']
                 #pprint(Issue_Type)

                 """
                 To Fetch Summary
                 """

                 summary = data['issue']['fields']['summary']
                 #pprint(summary)

                 """
                 To Fetch Description
                 """

                 description = data['issue']['fields']['description']
                 #pprint(description)

                 """
                 To Fetch Issue_Key
                 """

                 issue_key = data['issue']['key']
                 #pprint(issue_key)

                 """
                 To Fetch Due_date
                 """

                 duedate = data['issue']['fields']['duedate']
                 #pprint(duedate)

                 """
                 To Fetch Approvers name
                 """

                 Approvers = data['issue']['fields']['customfield_16406']
                 #pprint(Approvers[0]['name'])

                 """
                 To Fetch Priority  name
                 """
                 Priority = data['issue']['fields']['priority']['name']
                 #pprint(Priority)

                 """
                 Now It stores all the necessary Information to Json file called TicketInformation  
                 """


                 data ={


                            "blocks": [
                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": ":slack: *There is a request in Jira that requires your approval. Please find a summary here:*",

                                    }
                                },
                                {
                                    "type": "section",
                                    "fields": [
                                        {
                                            "type": "mrkdwn",
                                            "text": "*IssueKey:*\n%s"%issue_key
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Reporter:*\n%s"%Reporter.group(1)
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Summary:*\n%s"%summary
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Description:*\n%s"%description
                                        },

                                        {
                                            "type": "mrkdwn",
                                            "text": "*Issue_Type:*\n%s" % Issue_Type
                                        },


                                        {
                                            "type": "mrkdwn",
                                            "text": ":link:*For more details, follow this link to Jira*:point_down:"
                                                    "\n"
                                                    "https://jira-test.nentgroup.com/browse/%s" % issue_key
                                        }
                                    ]
                                },
                                {
                                    "type": "actions",
                                    "elements": [
                                        {
                                            "type": "button",
                                            "text": {
                                                "type": "plain_text",

                                                "text": "Approve"
                                            },
                                            "style": "primary",
                                            "value": "click_me_123"
                                        },
                                        {
                                            "type": "button",
                                            "text": {
                                                "type": "plain_text",

                                                "text": "Reject"
                                            },
                                            "style": "danger",
                                            "value": "click_me_123"
                                        }
                                    ]
                                }
                            ]
                        }




                 dir = os.path.dirname(__file__)
                 #pprint(dir)

                 """
                 First It clears previous data
                 """
                 print('This is deleting all data inside ')
                 with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/ticketInformation.json'.format(dir)) as json_file:
                     opendata = json.load(json_file)
                     opendata.clear()
                     #pprint(opendata)

                 """
                 it prints {} to start writing json
                 """

                 with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/ticketInformation.json'.format(dir), 'w') as json_file:
                     writedata = json.dump(opendata, json_file)
                     print('this is writing only {} inside file ')
                     #pprint(writedata)

                 """
                 It adds information about new ticket is requested
                 """

                 with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/ticketInformation.json'.format(dir), 'r+') as json_file:

                     ticketInformation = json.load(json_file)

                     ticketInformation.update(data)

                     json_file.seek(0)

                     json.dump(data, json_file)

                 #pprint(ticketInformation)
                 print('Stroring inside Json File  is done Successfully')

                 """
                 To send direct message to user it needs to split @sign + domain  email as suffixes
                 To convert any upper case letter into the Lower case in order to get recognised by Slack
                 Print name.family inside approverInfo json file 
                 """
                 regexStr = r'^([^@]+)@[^@]+$'
                 emailStr = Approvers[0]['name']
                 approver = re.search(regexStr, emailStr)
                 if not approver is None:
                     print(approver.group(1))
                 else:
                     print("Did not match")

                 print('this is approval name.family')
                 string = approver.group(1)
                 name_family = string.lower()
                 print('this is printing name and family', name_family)

                 datainfo = {}
                 print('this is printing datainfo', datainfo)
                 datainfo['Approver'] = []
                 datainfo['Approver'].append({
                     'name': '%s' % name_family
                 })

                 print('this is printing datainfo')
                 pprint(datainfo)
                 print('this is printing datainfo by appending Approver', '%s' % name_family)

                 datainfo['Issue_key'] = []
                 datainfo['Issue_key'].append({
                     'name': '%s' % issue_key
                 })

                 datainfo['Issue_Type'] = []
                 datainfo['Issue_Type'].append({
                     'name': '%s' % Issue_Type
                 })

                 datainfo['Summary'] = []
                 datainfo['Summary'].append({
                     'name': '%s' % summary
                 })

                 datainfo['Description'] = []
                 datainfo['Description'].append({
                     'name': '%s' % description
                 })

                 datainfo['Priority'] = []
                 datainfo['Priority'].append({
                     'name': '%s' % Priority
                 })
                 "this is changed direction for checking github in pipeline"
                 print('Here the approver name.family is storing into json file as approverInfo.json')
                 dir = os.path.dirname(__file__)
                 with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/approverInfo.json'.format(dir), 'w') as json_file:
                     file = json.dump(datainfo, json_file)
                 print('this is printing file')

                 message = 'Pure Approver name.family is exposed  Successfully'
                 connectToSlack()
                 print(message)
                 return make_response("OK", 200)



# The endpoint Slack will load your menu options from
@app1.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    print('Parse the request payload')

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])
    print('Verify that the request came from Slack')

    # Dictionary of menu options which will be sent as JSON
    menu_options = {
        "options": [
            {
                "text": "Approve",
                "value": "Approve"
            },
            {
                "text": "Reject",
                "value": "Reject"
            }
        ]
    }
    #pprint(menu_options)

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')

@app1.route('/slack/message_actions', methods=['POST'])
def message_actions():
        print('This is a Function which sends DM to Approver')
        slackResponse()
        # appUpdatesJira_commenting.statusUpdatesByCommenting()
        # print('This updating is Done succesfully')
        return make_response("OK", 200)


def connectToSlack():
    """
    1: It is reading ApproverInfor file to fetch name.family of Approver
    :return:
    """
    dir = os.path.dirname(__file__)
    # pprint(dir)
    with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/approverInfo.json', 'r') as json_file:
        filename = json.load(json_file)
    # pprint(filename)
    x = filename['Approver']
    string = x[0]['name']
    name_family = string.lower()
    print('this is printing name and family', name_family)

    """
    It is connecting to SLACK By Using API Token
    """
    App_Token = os.environ.get('App_Token')
    print(App_Token)
    slack_client = slack.WebClient(App_Token)
    print('API Connection is successfull')

    """This Json File has interactive message
       By opening and reading data to post Interactive message message
    """
    with open('/Users/reihvafa/Workspace/github_test_pipeline/listenerToJira/ticketInformation.json'.format(dir), 'r') as Interactive_json_file:
        interactive_message = json.load(Interactive_json_file)
    print('this is all ticket information for sending interactive message')
    # pprint(interactive_message)

    """With This conversation.list method we can list all channels in a Slack team.
    """

    channels_info = slack_client.api_call('conversations.list')
    # pprint(channels_info['channels'])
    channels = channels_info.get('channels') if channels_info else None
    # print('Print all channeles')
    # pprint(channels)

    """
    Lists all users in a Slack team by users.list method
    """
    users_identity = slack_client.api_call('users.list')
    print('this is printing all identity members')
    pprint(users_identity['members'])

    """Now it converts user name.family to its user id for posting dierct message to approver person 
    """

    if users_identity.get('ok'):
        for identity in users_identity.get('members'):

            pprint(identity.get("name"))
            if identity.get("name") == name_family:
                time.sleep(3)
                identity_channel = identity.get("id")
                print('this is printing all identity channel')
                pprint(identity_channel)
                print('this is posting message')
                slack_client.chat_postMessage(channel=identity_channel
                                              , attachments=[interactive_message])

                return make_response("OK", 200)


def slackResponse():
    """
             It is connecting to SLACK By Using API Token
             """
    App_Token = os.environ.get('App_Token')
    print(App_Token)
    slack_client = slack.WebClient(App_Token)
    # slack_client = slack.WebClient('xoxb-577663161824-1224571947153-QpntoV11hM4H8nhNg9tlX05t')
    print('API Connection is successfull')

    """This Json File has interactive message
       By opening and reading data to post Interactive message message
    """

    # dir = os.path.dirname(__file__)
    # with open(r'{0}/ticketInformation.json'.format(dir), 'r') as json_file:
    #     ReporterInfo = json.load(json_file)
    # pprint(ReporterInfo)

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    print('it is')
    pprint(form_json)

    print('this is printing all inform in playload')
    allInform = form_json['message']['attachments']
    # pprint(allInform)
    print('this is pringing blocks')
    blocks = allInform[0]
    # pprint(blocks)
    print('this is printing inside blocks')
    inside_block = blocks['blocks']
    # pprint(inside_block)
    print('this is printing lists ')
    list_block = inside_block[1]
    # pprint(list_block)
    # print('this is printing text')
    # pprint(list_block['fields'][0])

    approver = form_json['user']['name']
    # pprint(self.approver)

    IssueKey = list_block['fields'][0]['text']
    # print('this is printing text')
    # pprint(self.IssueKey)
    issue_key = IssueKey.replace('*IssueKey:*\n', '')
    # pprint(self.issue_key)

    Reporter = list_block['fields'][1]['text']
    # print('this is printing text')
    # pprint(self.Reporter)
    reporter = Reporter.replace('*Reporter:*\n', '')
    # pprint(self.reporter)

    Summary = list_block['fields'][2]['text']
    # pprint(self.Summary)
    summary = Summary.replace('*Summary:*\n', '')
    # pprint(self.summary)

    ts = form_json['message']
    # print('this is time stamp', self.ts['ts'])

    selection = form_json["actions"][0]
    # print(self.selection)

    # pprint(self.selection)
    # print('this is text text')
    # pprint(self.selection['text']['text'])

    if selection['text']['text'] == "Approve":
        message_text_approve = "Approve"

        data_Approve = {
            "blocks": [

                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Jira Ticket %s*" % issue_key

                    }
                }, {"type": "section",

                    "text": {

                        "text": ":white_check_mark: @%s %sd this request \n\n  " % (
                        approver, message_text_approve),
                        "type": "mrkdwn"
                    }

                    },

                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*IssueKey:*\n%s" % issue_key
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Summary:*\n%s" % summary
                        },
                        {
                            "type": "mrkdwn",
                            "text": ":link:*For more details, follow this link to Jira*:point_down:"
                                    "\n"
                                    "*Link*\nhttps://jira-test.nentgroup.com/browse/%s" % issue_key
                        }
                    ]
                }
            ]
        }

        slack_client.chat_update(channel=form_json["channel"]["id"],
                                 ts=ts['ts'], attachments=[data_Approve])
    elif selection['text']['text'] == "Reject":
        message_text_reject = "Reject"

        data_reject = {
            "blocks": [

                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Jira Ticket %s*" % issue_key

                    }
                }, {"type": "section",

                    "text": {

                        "text": ":white_check_mark: @%s %sd this request \n\n  " % (approver, message_text_reject),
                        "type": "mrkdwn"
                    }

                    },

                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*IssueKey:*\n%s" % issue_key
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Summary:*\n%s" % summary
                        },
                        {
                            "type": "mrkdwn",
                            "text": ":link:*For more details, follow this link to Jira*:point_down:"
                                    "\n"
                                    "*Link*\nhttps://jira-test.nentgroup.com/browse/%s" % issue_key
                        }
                    ]
                }
            ]
        }

        slack_client.chat_update(channel=form_json["channel"]["id"],
                                 ts=ts['ts'], attachments=[data_reject])

    print('This is a Function which Updates the Jira Ticket')
    #statusUpdatesByCommenting()
    jira = Jira(url='https://jira-test.nentgroup.com', username='jira-approvals-bot',
                password='DAthuzEc-3I6rabaru_o')

    # jira = Jira(url='https://jira-test.nentgroup.com', username='reihaneh.vafaei@nentgroup.com',
    #             password='Renistrong&1025')
    print('Connection is Done Sucessfully to Jira')
    print('Here the approver name.family is storing into json file as approverInfo.json')

    if selection['text']['text'] == "Approve":
        message_text_approve = "Approve"
        jira.issue_add_comment(issue_key,
                               ' This ticket is %sd in Slack by mailto:%s@nentgroup.com' % (
                                   message_text_approve, approver))
    elif selection['text']['text'] == "Reject":
        message_text_reject = "Reject"
        jira.issue_add_comment(issue_key, ' This ticket is %sed in Slack by mailto:%s@nentgroup.com' % (
            message_text_reject, approver))

    print('this commenting is done successfully')


    return make_response("OK", 200)


# def statusUpdatesByCommenting():
#     jira = Jira(url='https://jira-test.nentgroup.com', username='jira-approvals-bot',
#                 password='DAthuzEc-3I6rabaru_o')
#
#     # jira = Jira(url='https://jira-test.nentgroup.com', username='reihaneh.vafaei@nentgroup.com',
#     #             password='Renistrong&1025')
#     print('Connection is Done Sucessfully to Jira')
#     print('Here the approver name.family is storing into json file as approverInfo.json')
#
#     if selection['text']['text'] == "Approve":
#         message_text_approve = "Approve"
#         jira.issue_add_comment(issue_key,
#                                ' This ticket is %sd in Slack by mailto:%s@nentgroup.com' % (
#                                    message_text_approve, approver))
#     elif self.selection['text']['text'] == "Reject":
#         message_text_reject = "Reject"
#         jira.issue_add_comment(self.issue_key, ' This ticket is %sed in Slack by mailto:%s@nentgroup.com' % (
#             message_text_reject, self.approver))
#
#     print('this commenting is done successfully')


if __name__ == "__main__":

    print('Run app to parse data from Jira')
    app1.run()


