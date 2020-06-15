from flask import Flask
from flask import json
from flask import request, make_response
import jsonify


import traceback
from markupsafe import escape
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def api_root():
    return('Welcome To return')

@app.route('/github', methods=['POST'])
def api_jiraTest_message():


     print('this is test to check if it comes to this function')
     pprint(request.get_json())


     if json.dumps({'success': True}== 200)  and ({'ContentType': 'application/json'}):
        print('this is successful')
        pprint(request.get_json())



         #data_info= json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
         #pprint(data_info)
     # if request.headers['Content-Type'] == 'Application/json':
     #     print('this is content-type')
     #
     #     data_info =
     #
     #     data_info = json.dumps(request.json)
     #     pprint(data_info)
     #     return data_info

     # data = request.data
     # print('try to loads data in json')x
     # jdata = json.dumps(data)
     # pprint(jdata)
     #
     # try:
     #
     #
     #        if jdata['webhookEvent'] == 'jira:issue_created':
     #           ticket_key = jdata['issue']['key']
     #           print('Ticket: %s' %ticket_key)
     #        else:
     #            msg = 'Invalid JIRA hook event. It should be "jira:issue_created"'
     #            print(msg)
     #            return make_response(msg, 403)
     # except:
     #
     #        msg = 'Incorrect data! Can not parse to json format'
     #        print(msg)
     #        return make_response(msg, 500)



    # if request.headers(['webhookEvent']) == 'Issues':


    #     #
    #     print('It should print data in json')
    #     info_data =json.dumps(request.json)
    #     pprint(info_data)



    # data = request.data
    # print('print all data')
    # pprint(data)
    # try:
    #     jdata = json.loads(data)
    #
    #     if jdata['webhookEvent'] == 'jira:issue_created':
    #         ticket_key = jdata['issue']['key']
    #         ticket_summary = jdata['issue']['fields']['summary']
    #         ticket_priority = jdata['issue']['fields']['priority']['name']
    #         ticket_description = jdata['issue']['fields']['description']
    #         ticket_assignee_displayname = jdata['issue']['fields']['assignee']['displayName'] if \
    #         jdata['issue']['fields']['assignee'] else 'null'
    #         ticket_assignee_username = jdata['issue']['fields']['assignee']['name'] if jdata['issue']['fields'][
    #             'assignee'] else 'null'
    #         ticket_reporter_displayname = jdata['issue']['fields']['reporter']['displayName'] if \
    #         jdata['issue']['fields']['reporter'] else 'null'
    #         ticket_reporter_username = jdata['issue']['fields']['reporter']['name'] if jdata['issue']['fields'][
    #             'reporter'] else 'null'
    #
    #         print('Ticket: %s | %s' % (ticket_key, ticket_summary))
    #         print('Priority: %s' % ticket_priority)
    #         print('Description: %s' % ticket_description)
    #         print('Assignee: %s (%s)' % (ticket_assignee_displayname, ticket_assignee_username))
    #         print('Reporter: %s (%s)' % (ticket_reporter_displayname, ticket_reporter_username))
    #
    #         return make_response('ok', 200)
    #     else:
    #         msg = 'Invalid JIRA hook event. It should be "jira:issue_created"'
    #         print(msg)
    #         return make_response(msg, 403)
    # except:
    #     print(traceback.format_exc())
    #     msg = 'Incorrect data! Can not parse to json format'
    #     print(msg)
    #     return make_response(msg, 500)








    # if request.headers(['Events']) == 'project = "Viaplay Service Desk"':
    #     return json.dumps(request.json)



if __name__ == "__main__":

    app.run(debug=True)
    print('To run api-jiraTest_message')


