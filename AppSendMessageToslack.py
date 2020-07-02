from flask import Flask
from flask import json
from flask import request, make_response
import os
import slack
import time
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

         slack_client = slack.WebClient(os.environ.get('App_Token'))
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
                                          , attachments=[interactive_message], as_user=True)



if __name__ == "__main__":


    print('This function send direct message to Approver')
    connectToSlack()