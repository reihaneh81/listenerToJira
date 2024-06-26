from flask import Flask
from flask import json
from flask import request, make_response
import os

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
                         "text": ":slack: *Hello from JiraServiceDesk_Approval Slack APP*\n\n *It is Time to check the Jira ticket * "

                     }
                 },

                 {"type": "section",

                  "text": {

                      "text": "*This Jira Ticker %s* has requested you as an approver to check the description and confirm the Approval" % issue_key,
                      "type": "mrkdwn"
                  }
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

         print('this is approval name.family')
         string = approver.group(1)
         name_family = string.lower()
         print('this is printing name and family', name_family)

         datainfo ={}
         print('this is printing datainfo',datainfo)
         datainfo['Approver'] =[]
         datainfo['Approver'].append({
            'name': '%s'%name_family
         })

         print('this is printing datainfo')
         pprint(datainfo)
         print('this is printing datainfo by appending Approver','%s'%name_family)

         print('Here the approver name.family is storing into json file as approverInfo.json')
         dir = os.path.dirname(__file__)
         with open(r'{0}/approverInfo.json'.format(dir), 'w') as json_file:
            json.dump(datainfo, json_file)

         message = 'Pure Approver name.family is exposed  Successfully'

         print(message)




if __name__ == "__main__":


    print('To run app  to parse data from Jira')
    app1.run()








