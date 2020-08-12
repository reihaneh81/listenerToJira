from flask import Flask
from flask import json
from flask import request, make_response
import slack
import time
from slackeventsapi import SlackEventAdapter
from slack import WebClient

import os
#from slackeventsapi import SlackEventAdapter

from string import ascii_lowercase
import re
import jsonify
import approvalJiraTicket_Jira


import traceback
from markupsafe import escape
from pprint import pprint


def connectToSlack():


         """
         1: It is reading ApproverInfor file to fetch name.family of Approver
         :return:
         """


         dir = os.path.dirname(__file__)
         pprint(dir)
         with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
            filename = json.load(json_file)
         pprint(filename)
         x=filename['Approver']
         string = x[0]['name']
         name_family=string.lower()
         print('this is printing name and family', name_family)


         """
         It is connecting to SLACK By Using API Token
         """
         App_Token= os.environ.get('App_Token')
         print(App_Token)
         slack_client = slack.WebClient(App_Token)

         #slack_client = slack.WebClient('xoxb-577663161824-1224571947153-QpntoV11hM4H8nhNg9tlX05t')
         print('API Connection is successfull')

         """This Json File has interactive message
            By opening and reading data to post Interactive message message
         """

         with open(r'{0}/ticketInformation.json'.format(dir), 'r') as Interactive_json_file:
            interactive_message = json.load(Interactive_json_file)
         print('this is all ticket information for sending interactive message')
         pprint(interactive_message)

         """With This conversation.list method we can list all channels in a Slack team.
         """

         channels_info = slack_client.api_call('conversations.list')
         pprint(channels_info['channels'])
         channels = channels_info.get('channels') if channels_info else None
         print('Print all channeles')
         pprint(channels)


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

    print('Here the approver name.family is storing into json file as approverInfo.json')
    dir = os.path.dirname(__file__)
    with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
        ReporterInfo = json.load(json_file)
    pprint(ReporterInfo)
    pprint(ReporterInfo['Approver'])
    Reporter = ReporterInfo['Approver'][0]
    pprint(Reporter)
    pprint(Reporter['name'])



    issue_key = ReporterInfo['Issue_key'][0]
    pprint(issue_key)
    pprint(issue_key['name'])

    Issue_Type = ReporterInfo['Issue_Type'][0]
    pprint(Issue_Type)
    pprint(Issue_Type['name'])

    summary = ReporterInfo['Summary'][0]
    pprint(summary)
    pprint(summary['name'])

    description = ReporterInfo['Description'][0]
    pprint(description)
    pprint(description['name'])

    Priority = ReporterInfo['Priority'][0]
    pprint(Priority)
    pprint(Priority['name'])


    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    print('it is')
    pprint(form_json)

    ts =form_json['message']
    print('this is time stamp',ts['ts'])


    # Verify that the request came from Slack
    #verify_slack_token(form_json["token"])

    # Check to see what the user's selection was and update the message accordingly
    # selection = form_json["actions"][0]["text"][0]["value"]
    selection = form_json["actions"][0]
    print(selection)

    pprint(selection)

    if selection == "Approve":
        message_text = "Approve"
    else:
        message_text = "Reject"

    dir = os.path.dirname(__file__)
    with open(r'{0}/ticketInformation.json'.format(dir), 'r') as json_file:
        ReporterInfo = json.load(json_file)
    pprint(ReporterInfo)






    data2 = {
        "blocks": [

            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":slack: *Hello from JiraServiceDesk_Approval Slack APP*\n\n\n\n"

                }
            },

            {"type": "section",

             "text": {

                 "text": "You can check the Jira request that you approved with this following information and link  : \n\n https://jira-test.nentgroup.com/browse/%s"
                         
                         "\n\n"
                         "*Reporter*:             %s"
                         "\n\n"
                         "*Issue_Type*:             %s"
                         "\n\n"
                         "*Summary*:                %s"
                         "\n\n"
                         "*Description*:            %s"
                         "\n\n"
                         "*Issue_Key*:               %s"
                         "\n\n"
                         "*Priority*:                   %s"
                         "\n\n"
                         "" % (issue_key['name'],Reporter['name'],Issue_Type['name'], summary['name'], description['name'], issue_key['name'], Priority['name']),
                 "type": "mrkdwn"
             }
             }, {"type": "section",

             "text": {

                 "text": ":white_check_mark: @%s approved this request \n\n  "%Reporter['name'],
                 "type": "mrkdwn"
             }

             }
        ]
    }























    dataEx={
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "This is a plain text section block."

			}
		}
	]
}

    pprint(data2)
    # return slack_client.chat_update(
    #
    #     channel=form_json["channel"]["id"],
    #     ts='1234567890.123456',
    #     text="One {}, right coming up! :coffee:".format(message_text),
    #     attachments=[dataEx]
    # )

    slack_client.chat_update(channel=form_json["channel"]["id"],
               ts=ts['ts'],attachments=[data2])

    return make_response("OK", 200)


if __name__ == "__main__":


    print('This function send direct message to Approver')
    connectToSlack()


