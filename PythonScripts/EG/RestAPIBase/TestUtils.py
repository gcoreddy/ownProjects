import RestAPIBase
from RallyRestInterface import RallyRestInterface
from JiraRestInterface import JiraRestInterface


class TestUtils(RallyRestInterface):

    def __init__(self,  server, user, project, workspace, interface_type, password):
        super(TestUtils, self).__init__(server, user, project, workspace, interface_type, password)
        """Return a new Rally object."""
        self.server = server
        self.user = user
        self.password = password
        self.workspace = workspace
        self.project = project
        self.interface_type = interface_type


test = TestUtils('rally1.rallydev.com', 'govardhan.yadav@amd.com', 'Ultrasound', 'AMD', 'Rally', 'Way2go@527')

rallyobj = test.interface_obj('rally1.rallydev.com', 'govardhan.yadav@amd.com', 'Ultrasound', 'AMD', 'Rally',
                              'Way2go@527')
##
user_story_list = ['US3488','US3501','US3485','US4182'] #'US4148'
for us in user_story_list:
    """Pull the tclist and update the results"""
    puller = test.ipuller(rallyobj, 'UserStory', us)
    tc_dict = test.iexecutor(puller)
    tc_upater = test.iupdater(tc_dict)


