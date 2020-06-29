from flask import Flask
from flask import json
from flask import request, make_response
import os
import AppSendMessageToslack
import logging
import slack
import re
from pprint import pprint


"""This is name Of Application 
   The one we are going to listening
"""
app1 = Flask(__name__)


"""
     This is route of App as a simple example which display the message on web when we run app it
"""





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
                                "value": "click_me_456"
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

         with open(r'{0}/ticketInformation.json'.format(dir), 'r+') as json_file:

             ticketInformation = json.load(json_file)

             ticketInformation.update(data)

             json_file.seek(0)

             json.dump(data, json_file)

         pprint(ticketInformation)

         print('Stroring is done Successfully')

         """
         Its splits @sign + domain  email
         """
         regexStr = r'^([^@]+)@[^@]+$'
         emailStr = Approvers[0]['name']
         approver = re.search(regexStr, emailStr)
         if not approver is None:
             print(approver.group(1))
         else:
             print("Did not match")

         datainfo ={}
         print('this is printing datainfo',datainfo)
         datainfo['Approver'] =[]
         datainfo['Approver'].append({
            'name': '%s'%approver.group(1)
         })
         print('this is printing datainfo by appending Approver','%s'%approver.group(1))

         print('Here the approver name.family is storing into json file as approverInfo.json')
         dir = os.path.dirname(__file__)
         with open(r'{0}/approverInfo.json'.format(dir), 'w') as json_file:
            json.dump(datainfo, json_file)

         message = 'Pure Approver name.family is exposed  Successfully'
         AppSendMessageToslack.connectToSlack()
         print(message)




if __name__ == "__main__":


    print('To run app  to parse data from Jira')
    app1.run()
