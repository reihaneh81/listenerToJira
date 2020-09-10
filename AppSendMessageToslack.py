
from atlassian import Jira
from flask import json
from flask import request, make_response
import slack
import time
import os
from pprint import pprint


class AppToSlack():

            def connectToSlack(self):
                """
                1: It is reading ApproverInfor file to fetch name.family of Approver
                :return:
                """
                dir = os.path.dirname(__file__)
                #pprint(dir)
                with open(r'{0}/approverInfo.json'.format(dir), 'r') as json_file:
                    filename = json.load(json_file)
                #pprint(filename)
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
                with open(r'{0}/ticketInformation.json'.format(dir), 'r') as Interactive_json_file:
                    interactive_message = json.load(Interactive_json_file)
                print('this is all ticket information for sending interactive message')
                #pprint(interactive_message)

                """With This conversation.list method we can list all channels in a Slack team.
                """

                channels_info = slack_client.api_call('conversations.list')
                #pprint(channels_info['channels'])
                channels = channels_info.get('channels') if channels_info else None
                #print('Print all channeles')
                #pprint(channels)

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


            def slackResponse(self):
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
                #pprint(allInform)
                print('this is pringing blocks')
                blocks = allInform[0]
                #pprint(blocks)
                print('this is printing inside blocks')
                inside_block = blocks['blocks']
                #pprint(inside_block)
                print('this is printing lists ')
                list_block = inside_block[1]
                #pprint(list_block)
                # print('this is printing text')
                # pprint(list_block['fields'][0])


                self.approver =form_json['user']['name']
                #pprint(self.approver)


                self.IssueKey=list_block['fields'][0]['text']
                # print('this is printing text')
                # pprint(self.IssueKey)
                self.issue_key = self.IssueKey.replace('*IssueKey:*\n', '')
                # pprint(self.issue_key)

                self.Reporter =list_block['fields'][1]['text']
                # print('this is printing text')
                # pprint(self.Reporter)
                self.reporter= self.Reporter.replace('*Reporter:*\n','')
                # pprint(self.reporter)

                self.Summary =list_block['fields'][2]['text']
                #pprint(self.Summary)
                self.summary = self.Summary.replace('*Summary:*\n','')
                #pprint(self.summary)


                self.ts = form_json['message']
                #print('this is time stamp', self.ts['ts'])

                self.selection = form_json["actions"][0]
                #print(self.selection)

                # pprint(self.selection)
                # print('this is text text')
                # pprint(self.selection['text']['text'])


                if self.selection['text']['text'] == "Approve":
                    message_text_approve = "Approve"


                    data_Approve = {
                            "blocks": [

                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text":"*Jira Ticket %s*"%self.issue_key

                                    }
                                }, {"type": "section",

                                     "text": {

                                         "text": ":white_check_mark: @%s %sd this request \n\n  " % (self.approver,message_text_approve),
                                         "type": "mrkdwn"
                                     }

                                     },

                                {
                                    "type": "section",
                                    "fields": [
                                        {
                                            "type": "mrkdwn",
                                            "text": "*IssueKey:*\n%s" % self.issue_key
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Summary:*\n%s" % self.summary
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": ":link:*For more details, follow this link to Jira*:point_down:"
                                                                "\n"
                                                    "*Link*\nhttps://jira-test.nentgroup.com/browse/%s" % self.issue_key
                                        }
                                    ]
                                }
                            ]
                        }

                    slack_client.chat_update(channel=form_json["channel"]["id"],
                                             ts=self.ts['ts'], attachments=[data_Approve])
                elif self.selection['text']['text'] ==  "Reject":
                        message_text_reject = "Reject"



                        data_reject = {
                                "blocks": [

                                {
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text":"*Jira Ticket %s*"%self.issue_key

                                    }
                                }, {"type": "section",

                                     "text": {

                                         "text": ":white_check_mark: @%s %sd this request \n\n  " % (self.approver,message_text_reject),
                                         "type": "mrkdwn"
                                     }

                                     },

                                {
                                    "type": "section",
                                    "fields": [
                                        {
                                            "type": "mrkdwn",
                                            "text": "*IssueKey:*\n%s" % self.issue_key
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Summary:*\n%s" % self.summary
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": ":link:*For more details, follow this link to Jira*:point_down:"
                                                                "\n"
                                                    "*Link*\nhttps://jira-test.nentgroup.com/browse/%s" % self.issue_key
                                        }
                                    ]
                                }
                            ]
                        }


                        slack_client.chat_update(channel=form_json["channel"]["id"],
                                         ts=self.ts['ts'], attachments=[data_reject])

                print('This is a Function which Updates the Jira Ticket')
                self.statusUpdatesByCommenting()

                return make_response("OK", 200)


            def statusUpdatesByCommenting(self):


                jira = Jira(url='https://jira-test.nentgroup.com', username='jira-approvals-bot',
                            password='DAthuzEc-3I6rabaru_o')

                # jira = Jira(url='https://jira-test.nentgroup.com', username='reihaneh.vafaei@nentgroup.com',
                #             password='Renistrong&1025')
                print('Connection is Done Sucessfully to Jira')
                print('Here the approver name.family is storing into json file as approverInfo.json')

                if self.selection['text']['text'] == "Approve":
                    message_text_approve = "Approve"
                    jira.issue_add_comment(self.issue_key,
                                           ' This ticket is %sd in Slack by mailto:%s@nentgroup.com' % (
                                           message_text_approve, self.approver))
                elif self.selection['text']['text'] == "Reject":
                    message_text_reject = "Reject"
                    jira.issue_add_comment(self.issue_key, ' This ticket is %sed in Slack by mailto:%s@nentgroup.com' % (
                    message_text_reject, self.approver))

                print('this commenting is done successfully')
