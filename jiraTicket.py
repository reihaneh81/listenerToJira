from flask import Flask
from flask import json
from flask import request, make_response,Response
import os
import AppSendMessageToslack
from slackeventsapi import SlackEventAdapter
import logging
import slack
import re
from pprint import pprint


"""This is name Of Application 
   The one we are going to listen
"""
app1 = Flask(__name__)


"""
     This is route of App as a simple example which display the message on web when we run app it
"""


# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
print('this is SLACK_SIGNING_SECRET',slack_signing_secret)


SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]



# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ["App_Token"]
print('This is SLACK_BOT_TOKEN ',slack_bot_token)
slack_client = slack.WebClient(slack_bot_token)

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
    to post data to app which is comig from Jira , to that I set up the webhook url by using ngrok/webhook , 
    which allows to post data in real time when the new Jira ticket is created and we can sort of split 
    which kinds of information we need to  receive such as IssueTyoe, Summary/description, Reporter name and 
    the main part Approval name.family
"""
@app1.route('/webhook', methods=['POST'])
def api_jiraTest_message():


         data = request.get_json()


         """
         To Fetch Reporter name
         """
         Reporter = data['issue']['fields']['reporter']
         print('All the information about Reporter')
         pprint(Reporter)
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
             print('print name and familyname of reporter',Reporter.group(1))
         else:
             print("Did not match")

         """
         To Fetch Issue Type
         """
         Issue_Type = data['issue']['fields']['issuetype']['name']
         pprint(Issue_Type)

         """
         To Fetch Summary
         """

         summary = data['issue']['fields']['summary']
         pprint(summary)

         """
         To Fetch Description
         """

         description = data['issue']['fields']['description']
         pprint(description)

         """
         To Fetch Issue_Key
         """

         issue_key = data['issue']['key']
         pprint(issue_key)

         """
         To Fetch Due_date
         """

         duedate = data['issue']['fields']['duedate']
         pprint(duedate)

         """
         To Fetch Approvers name
         """

         Approvers = data['issue']['fields']['customfield_16406']
         pprint(Approvers[0]['name'])

         """
         To Fetch Priority  name
         """
         Priority = data['issue']['fields']['priority']['name']
         pprint(Priority)


         """
         Now It stores all the necessary Information to Json file called TicketInformation  
         """


         data = {
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

                      "text": "You have a new Jirat Ticket request to approve from @%s\n\n Please check the Jira request with this following information and link : \n\n https://jira-test.nentgroup.com/browse/%s"
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
                              "" % (Reporter.group(1),issue_key,Issue_Type,summary,description,issue_key,Priority),
                      "type": "mrkdwn"
                  }
                  },{
                        "type": "actions",
                        "block_id": "actionblock789",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Approve"
                                },
                                "style": "primary",
                                "value": "Approve"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Reject"
                                },

                            }
                        ]
                    }
                         ]
                     }








         pprint(data)

         dir = os.path.dirname(__file__)
         pprint(dir)


         """
         First It clears previous data
         """


         with open(r'{0}/ticketInformation.json'.format(dir)) as json_file:
             opendata= json.load(json_file)
             opendata.clear()

             print('this is deleting all data inside ')
             pprint(opendata)

         """
         it prints {} to start writing json
         """

         with open(r'{0}/ticketInformation.json'.format(dir), 'w') as json_file:
             writedata = json.dump(opendata,json_file)
             print('this is writing only {} inside file ')
             pprint(writedata)


         """
         It adds information about new ticket is requested
         """

         with open(r'{0}/ticketInformation.json'.format(dir), 'r+') as json_file:

             ticketInformation = json.load(json_file)

             ticketInformation.update(data)

             json_file.seek(0)

             json.dump(data, json_file)

         pprint(ticketInformation)

         print('Stroring is done Successfully')

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



         print('Here the approver name.family is storing into json file as approverInfo.json')
         dir = os.path.dirname(__file__)
         with open(r'{0}/approverInfo.json'.format(dir), 'w') as json_file:
            file=json.dump(datainfo, json_file)
         print('this is printing file')

         message = 'Pure Approver name.family is exposed  Successfully'
         AppSendMessageToslack.connectToSlack()
         print(message)
         #verify_slack_token(request_token=SLACK_VERIFICATION_TOKEN)
         #slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")
         #incoming_slack_message()
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
    pprint(menu_options)

    # Load options dict as JSON and respond to Slack
    return Response(json.dumps(menu_options), mimetype='application/json')

@app1.route('/slack/message_actions', methods=['POST'])
def message_actions():



        AppSendMessageToslack.slackResponse()
        return make_response("OK", 200)


        #     # data = request.get_json()
        #     #
        #     # """
        #     # To Fetch Reporter name
        #     # """
        #     # Reporter = data['issue']['fields']['reporter']
        #     # print('All the information about Reporter')
        #     # pprint(Reporter)
        #     # Reporter_name = Reporter['name']
        #     # print('this is print reporter name')
        #     # pprint(Reporter_name)
        #     #
        #
        #     print('Here the approver name.family is storing into json file as approverInfo.json')
        #     dir = os.path.dirname(__file__)
        #     with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
        #         ReporterInfo=json.load(json_file)
        #     pprint(ReporterInfo)
        #     pprint(ReporterInfo['Approver'])
        #     Reporter =ReporterInfo['Approver'][0]
        #     pprint(Reporter)
        #     pprint(Reporter['name'])
        #
        #     # """
        #     # Its splits @sign + domain  email
        #     # """
        #     # regexStr = r'^([^@]+)@[^@]+$'
        #     # emailStr = Reporter['name']
        #     # Reporter = re.search(regexStr, emailStr)
        #     # if not Reporter is None:
        #     #     print('print name and familyname of reporter', Reporter.group(1))
        #     # else:
        #     #     print("Did not match")
        #
        # # Parse the request payload
        #     form_json = json.loads(request.form["payload"])
        #     print('it is')
        #
        #     # Verify that the request came from Slack
        #     verify_slack_token(form_json["token"])
        #
        #     # Check to see what the user's selection was and update the message accordingly
        #     #selection = form_json["actions"][0]["text"][0]["value"]
        #     selection = form_json["actions"][0]["value"]
        #
        #     pprint(selection)
        #
        #     if selection == "Approve":
        #         message_text = "Approve"
        #     else:
        #         message_text = "Reject"
        #
        #     data2 = {
        #         "blocks": [
        #
        #             {
        #                 "type": "section",
        #                 "text": {
        #                     "type": "mrkdwn",
        #                     "text": ":slack: *Hello from JiraServiceDesk_Approval Slack APP*\n\n\n\n"
        #
        #                 }
        #             },
        #
        #             {"type": "section",
        #
        #              "text": {
        #
        #               "text": "@%s approved this request \n\n  " % (Reporter['name']),
        #               "type": "mrkdwn"
        #           }
        #
        #           }
        #     ]
        #     }
        #
        #
        #
        #
        #     pprint(data2)
        #     return slack_client.chat_update(
        #
        #       channel=form_json["channel"]["id"],
        #       ts='1234567890.123456',
        #       text="One {}, right coming up! :coffee:".format(message_text),
        #       attachments=[data2] # empty `attachments` to clear the existing massage attachments
        #     )
        #
        #     # Send an HTTP 200 response with empty body so Slack knows we're done here
        #
        #     #return slack_client.chat_postMessage(channel=identity_channel
        #                                          #, attachments=[interactive_message])
        #     #return make_response("", 200)
        #



# @app1.route('/slack/events', methods=['POST'])
# def incoming_slack_message():
#              statement = None
#              slack_req = json.loads(request.form.get('payload'))
#              response = '{"text": "Hi, <@' + slack_req["user"]["id"] + '>"}'Pure Approver name.family is exposed  Successfully
#              user = slack_req["user"]["name"]
#              user_response = slack_req["actions"][0]["value"]
#              orig_message = slack_req["original_message"]
#
#              if user_response == "yes":
#                  statement = user + "chose " + user_response
#
#              print(slack_req)
#
#              orig_message['attachments'][0]['text'] = statement + "\n"
#              return Response(response=json.dumps(orig_message), status=200, mimetype="application/json")


         # # Example responder to greetings
         # @slack_events_adapter.on("message")
         # def handle_message(event_data):
         #        message = event_data["event"]
         #        # If the incoming message contains "hi", then respond with a "Hello" message
         #        if message.get("subtype") is None and "Approve" in message.get('text'):
         #            channel = message["channel"]
         #            message = "Hello <@%s>! :tada:" % message["user"]
         #            slack_client.chat_postMessage(channel=channel, text=message)





if __name__ == "__main__":


    print('To run app  to parse data from Jira')
    app1.run()
