
import random
import webapp3
import slack
import os
import time
from pprint import pprint


class Home(webapp3.RequestHandler):
    """
    This Class (Home) inherents from webapp2 module by object RequestHandler
    :return:
    """
    def get(self):
        """
        simply response to get request by this function
        :return:
        """

        self.response.write("Hello, R&DHer, R&DHIM Viewers")



class R52MeetingRooms(webapp3.RequestHandler):

    def post(self):

        room= self.request.get('text')
        r52MeetingRooms(room,self)
        #directmessageByIMLIST(self)

def r52MeetingRooms(room, self):

    self.development_id = 'CRJKN06AH'
    self.random_id = 'CH348L8P9'
    self.Gustav_id = 'UH213SCS0'
    self.reihaneh_Id = 'UR4N35W1F'
    self.slackbot_Id = 'USLACKBOT'
    self.Employee_manager = 'reihaneh.vafaei'
    self.slacktest_name = 'slack.testaccount'
    self.day_to_run = 27
    self.month_to_run = 1


    self.slack_client = slack.WebClient('xoxb-577663161824-864692303857-3owjOZrhXnmmh1h1ZCEhdwQR')
    print('API Connection is successfull')
    self.dir = os.path.dirname(__file__)
    print(self.dir)

    self.file_Universe = r'{0}/pictures/Universe.jpeg'.format(self.dir)
    self.file_Fireplace = r'{0}/pictures/Fireplace.jpeg'.format(self.dir)

    time.sleep(3)

    if room == "Universe":
        users_identity = self.slack_client.api_call('users.list')
        pprint(users_identity['members'])

        if users_identity.get('ok'):
            for identity in users_identity.get('members'):
                print('This is identity', identity)
                print(identity.get("name"))
                # if identity.get("name") == self.user['New_Employee']:



                if identity.get("name") == 'reihaneh.vafaei':
                    self.identity_channel = identity.get("id")

                    pprint(self.identity_channel)



                    self.slack_client.files_upload(
                                                    file=self.file_Universe,
                                                                        initial_comment=":slack: *Hello from Pre-Onboarding Slack APP*\n\n"
                                                                          "*:point_right: Please use the Elevator on the right side of the Reception*\n\n"
                                                                          "*:point_right: Go to the Floor 7*\n\n"
                                                                          "*:point_right: Go to the Left :arrow_left: side and keep walking then you can see the Universe room at the end of the corridor*\n\n"
                                                                          "*:point_down: This is Universe Meeting room*",
                                                                        channels=self.identity_channel)

    elif room == "Fireplace":

        users_identity = self.slack_client.api_call('users.list')
        pprint(users_identity['members'])

        if users_identity.get('ok'):
            for identity in users_identity.get('members'):
                print('This is identity', identity)
                print(identity.get("name"))
                # if identity.get("name") == self.user['New_Employee']:

                if identity.get("name") == 'reihaneh.vafaei':
                    self.identity_channel = identity.get("id")

                    pprint(self.identity_channel)

                    self.slack_client.files_upload(
                                                    file=self.file_Fireplace,
                                                    initial_comment=":slack: *Hello from Pre-Onboarding Slack APP*\n\n"
                                                                    "*:point_right: Please use the Elevator on the right side of the Reception*\n\n"
                                                                    "*:point_right: Go to the Floor 7*\n\n"
                                                                    "*:point_right: Go to the Caffe machine and you can see the Fireplace room right in fron of the Caffe Machine*\n\n"
                                                                    "*:point_down: This is Fireplace Meeting room*",
                                                    channels=self.identity_channel)



"""
A WSGI-compliant application
#: Allowed request methods.
"""
app = webapp3.WSGIApplication(
    [
        (r'/', Home),
        (r'/r52meetingrooms',R52MeetingRooms)
    ]
)




def main():

    from paste import httpserver

    httpserver.serve(app, host='127.0.0.1', port='8080')



if __name__ == '__main__':

    main()



