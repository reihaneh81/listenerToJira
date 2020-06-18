from flask import Flask
from flask import json
from flask import request, make_response
import os
import slack
import re
import jsonify


import traceback
from markupsafe import escape
from pprint import pprint


#class FetchDataFromJiraTicket(object):


app1 = Flask(__name__)
@app1.route('/')
def api_root():

    return('Welcome To return')

@app1.route('/webhook', methods=['POST'])
def api_jiraTest_message():
    ############################# START TO SEND DIRECT MESSAGE TO  SLACK BY PARSING DATA FETCHED FROM JIRA ###############################





         print('this is test to check if it comes to this function')
         data = request.get_json()



         print('It is printing Issue Type')
         Issue_Type = data['issue']['fields']['issuetype']['name']
         pprint(Issue_Type)

         print('It is printing summary')
         summary = data['issue']['fields']['summary']
         pprint(summary)

         print('It is printing description')
         description = data['issue']['fields']['description']
         pprint(description)

         print('It is printing issue_key')
         issue_key = data['issue']['key']
         pprint(issue_key)

         print('It is printing issue_type')
         issue_type = data['issue']['fields']['issuetype']['name']
         pprint(issue_type)

         print('It is printing Approvers')
         Approvers = data['issue']['fields']['customfield_16406']
         pprint(Approvers)
         print('This is printing the name of approver')
         pprint(Approvers[0]['name'])

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

         print('Stroring is Successfull')





if __name__ == "__main__":

    # x= FetchDataFromJiraTicket()
    # x.app1.run()
    # x.api_root()
    # x.api_jiraTest_message()
    # x.toFetch_Name_Family()
    print('To run api-jiraTest_message')
    app1.run()






