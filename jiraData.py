from  approvalJiraTicket_Jira import api_jiraTest_message
from pprint import pprint

def interactivemessage():
    x0 =api_jiraTest_message()
    pprint(x0.issue_key)
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

                 "text": "*This Jira Ticker %s* has requested you to check the description and confirm the Approval" % x,
                 "type": "mrkdwn"
             }
             }
        ]
    }

    pprint(data)

interactivemessage()