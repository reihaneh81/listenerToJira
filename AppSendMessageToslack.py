from flask import Flask
from flask import json
from flask import request, make_response
import os
import slack
import re
import jsonify
import approvalJiraTicket_Jira


import traceback
from markupsafe import escape
from pprint import pprint

def connectToSlack():


         print('It is printing Interaction Message which is written in json format')


         dir = os.path.dirname(__file__)
         pprint(dir)
         with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
            filename = json.load(json_file)
         pprint(filename)
         x=filename['Approver']
         pprint(x)
         pprint(x[0])
         pprint(x[0]['name'])


         print('This is Slack Authentication Code')
         slack_client = slack.WebClient(os.environ.get('App_Token'))

         print('API Connection is successfull')

         """This Json File has interactive message
            By opening and inserting in Posting message
         """

         with open(r'{0}/ticketInformation.json'.format(dir), 'r') as Interactive_json_file:
            interactive_message = json.load(Interactive_json_file)
         pprint(interactive_message)



         channels_info = slack_client.api_call('conversations.list')

         pprint(channels_info['channels'])
         channels = channels_info.get('channels') if channels_info else None

         print('Print all channeles')
         pprint(channels)



         users_identity = slack_client.api_call('users.list')
         pprint(users_identity['members'])

         if users_identity.get('ok'):
          for identity in users_identity.get('members'):

           pprint(identity.get("name"))
           if identity.get("name") == x[0]['name']:
            # if identity.get("name") == 'reihaneh.vafaei':
            identity_channel = identity.get("id")
            pprint(identity_channel)

            slack_client.chat_postMessage(channel=identity_channel
                                          , attachments=[interactive_message],username=x[0]['name'], as_user=True)



if __name__ == "__main__":


    print('This function send direct message to Approver')
    connectToSlack()