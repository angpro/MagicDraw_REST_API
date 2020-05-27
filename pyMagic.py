import requests
import json

from model_data import username, password, project_url
import sys

# Running code :
#   import pyMagic
#  a = pyMagic.pyMagic('dd', 'ff', 'ff')
#  a.info


class pyMagic:
    # Class to hold methods to interface with MagicDraw model
    # project_url - main link at which model is clocated
    # Username / password - credentials to login into MagicDraw
    # Swarm CubeSat URL: project_url = "https://10.30.254.66:8111/osmc/workspaces/4d6ce495-1273-452c-a548-36fcd922184e/resources/1f4b1466-698e-4365-886b-1401c7d0bbeb"

    # project_url is where all branches and revisions of the project are located
    # model_url is pointing to the latest version of the model

    def __init__(self):
        self.project_url = project_url
        # These two have to be hidden to the outside
        self.username = username
        self.password = password

        # Also useful to suppress useless warnings
        if not sys.warnoptions:
             import warnings
             warnings.simplefilter("ignore")


    def info(self):
        print( self.project_url )
        # In principle can also print information such as latest branch, latest revision number of elements loaded
        # print( "Last branch", self.last_branch )
        # print( "Last revision", self.last_rev )

    def connect(self, model_name):
        # Initialization: get a session running
        # There is a timeout on connection, so it is better to have a new session before each request
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.get(self.project_url, verify=False)
        #
        print(self.project_url + '/branches')
        try:
            # branches_ptr = json.loads(self.session.get(self.project_url + '/branches').text)
            branches_ptr = self.session.get(self.project_url + '/branches').json()
        except json.decoder.JSONDecodeError:
            print(" JSONDecodeError")
            print( self.session.get(self.project_url + '/branches').text )
            # print( self.username, self.password)
        # Note that here we're picking up the first branch of the model.
        # TODO: idnetify all branches of the model.
        first_branch = json.loads(self.session.get(
            self.project_url  + '/branches/' + branches_ptr['ldp:contains'][0]['@id']).text)
        self.first_branch = branches_ptr['ldp:contains'][0]['@id']
        self.last_rev = first_branch[0]['ldp:contains'][0]

        #print(self.project_url  + '/branches/' + self.first_branch +
        # '/revisions/' + str(self.last_rev) )
         # This is description of all the stuff in the last version.
        last_rev = json.loads(self.session.get(
             self.project_url + '/branches/' + self.first_branch +
             '/revisions/' + str(self.last_rev) ).text)

        self.model_uuid = last_rev[0]['rootObjectIDs'][0]

        model_dir= {'base': '0xxdf'}

        # The rest is not neeeded; but can be useful for information.
        for m in last_rev[0]['rootObjectIDs'] :
            model_base = json.loads(self.session.get(
                 self.project_url + '/branches/' + self.first_branch +
                 '/revisions/' + str(self.last_rev) + '/elements/' + m).text)
            # print(self.project_url + '/branches/' + self.first_branch +
            # '/revisions/' + str(self.last_rev) + '/elements/' + m )
            # print(model_base[1]['@type'])
            eltype = model_base[1]['@type']
            if eltype == 'esiproject:EsiProject' :
                model_dir[ model_base[1]['kerml:name'] ] = m
            # print( model_base[1]['kerml:name'], m )

        # print( model_dir )
        print( 'UUID for the model', model_dir[ model_name ] )
        self.latest_model_uuid = model_dir[ model_name ]

        # Now from the link above we need to figure out which one is the model there
        # Keep this link as the root link to the model.

        #self.main_model = json.loads(self.session.get(
        #   self.project_url  + '/branches/' + self.first_branch +
        #        '/revisions/' + str(self.last_rev)).text)
        #print(self.project_url  + '/branches/' + branches_ptr['ldp:contains'][0]['@id'] +
        #'/revisions/' + str(self.first_branch))
        print(self.last_rev, self.first_branch)

    def get_element(self, element_id):
        model_element = json.loads(self.session.get(
            self.project_url + '/branches/' + self.first_branch +
            '/revisions/' + self.last_rev + '/elements/' + element_id).text)

    def model_traverse(self, model_base):
        print("TEST")
        print(model_base)
        print(model_base[1])

        # for m in model_base[0]['ldp:contains']:
        #     model_element_uuid = m['@id']
        #     model_element = self.get_element( model_element_uuid )
        #     # print( model_element_uuid, list(model_element[1]) )
        #     if 'kerml:name' in list(model_element[1]): print( model_element_uuid, model_element[1]['kerml:name'])
        #     # element_traverse( model_element )


if __name__ == "__main__":
    import sys
    # import pyMagic

    # In principle logic is like this:
    #    We have an element in the model named "Status" with certain values
    #    We have to locate it inside: workspace / model / revision of the model / find in the tree
    #    Find UUID of the element / change it to whatever we want.

    # TODO: Find proejct in the workspaces by name.

    model = pyMagic()

    # print( model.username )
    model.connect('Swarm_CubeSat_Project')

    model.model_traverse( model.latest_model_uuid )

    # Next steps:
    # el_uuid = model.search( 'Whatever the element called')
    # el_info = model.get_element( el_uuid )
    # Chaange whatever we need in the element, probably right in the el_info
    # model.post_element( el_uuid, el_info )
