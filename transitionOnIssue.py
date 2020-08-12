from jira import JIRA
from pprint import pprint





def statusUpdates():

    server = {'server' : 'http://jira-test.nentgroup.com'}
    #jira = JIRA(server)
    jira = JIRA(server,basic_auth=('reihaneh.vafaei@nentgroup.com', 'Renistrong&1025'))
                #,
                #basic_auth=('reihaneh.vafaei@nentgroup.com', 'Renistrong&1025'))
    print('Connection is Done Sucessfully to Jira')


    print('this goes to')

    #jira = JIRA('https://jira-test.nentgroup.com')

    issue = jira.issue("VPSD-3711")
    transitions = jira.transitions(issue)
    print('this shows the transition')
    pprint(transitions)

    # Resolve the issue and assign it to 'pm_user' in one step
    print('Resolve the issue and assign it to pm_user in one step')
    jira.transition_issue(issue, '51', assignee={'name': 'reihaneh vafaei'}, resolution={'id': '3'})

    pprint(transitions)




    print('this is approving ')
    jira.transition_issue(issue, transition='Fix Verfied')
    #print('this is printing jira id',issue.id)

    print('this went successfully')




if __name__ == "__main__":


    print('this is ')

    statusUpdates()