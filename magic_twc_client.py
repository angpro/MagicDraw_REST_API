import requests


class MagicClient:
    def __init__(self, username: str, pwd: str, twc_address: str):
        self.username = username
        self.pwd = pwd
        self.twc_address = twc_address

        # use it by default "Uncategorized" workspace
        # TODO: add option to select workspace by name
        self.workspace_id = "4d6ce495-1273-452c-a548-36fcd922184e"

        # use it by default "Swarm CubeSat" project
        # TODO: add option to select project by name
        self.project_id = "1f4b1466-698e-4365-886b-1401c7d0bbeb"

        self.last_revision = ""
        self.first_branch = ""

        self.session = None
        self._login()

        # self.get_projects_url = f"https://{self.twc_address}/osmc/workspaces/{self.workspace_id}"
        self.get_project_url = f"https://{self.twc_address}/osmc/workspaces/" \
                                        f"{self.workspace_id}/resources/{self.project_id}"

    def _login(self):
        self.session = requests.Session()
        self.session.auth = (self.username, self.pwd)

    # get model with first branch and last version
    # TODO: it is possible to find different version on different branches
    def get_model_id(self) -> str:
        get_project_branch_url = f"{self.get_project_url}/branches"

        branches = self.session.get(get_project_branch_url, verify=False).json()

        self.first_branch = branches['ldp:contains'][0]['@id']

        get_branch_revisions_url = f"{self.get_project_url}/branches/{self.first_branch}"
        revisions = self.session.get(get_branch_revisions_url, verify=False).json()
        self.last_revision = revisions[0]['ldp:contains'][0]

        get_project_last_revision_url = f"{self.get_project_url}/branches/{self.first_branch}/revisions/{self.last_revision}"
        project_last_revision = self.session.get(get_project_last_revision_url, verify=False).json()
        model_id = project_last_revision[0]['rootObjectIDs'][0]
        return model_id

    def uml_model_id(self) -> str:
        esi_project_id = ""
        model = self.get_element_body(self.get_model_id())

        for unit in model[1]["kerml:ownedElement"]:
            element_id = unit["@id"]
            element = self.get_element_body(element_id)

            if "kerml:esiData" in element[1] and "name" in element[1]["kerml:esiData"] and element[1]["kerml:esiData"]["name"] == "UML Model":
                esi_project_id = element[1]["kerml:esiData"]["sections"][0]["@id"]

        if esi_project_id:
            esi_project = self.get_element_body(esi_project_id)
            uml_model_id = esi_project[1]["kerml:esiData"]["rootElements"][0]
            return uml_model_id

    def get_element_body(self, element_id: str) -> dict:
        get_element_url = f"{self.get_project_url}/branches/{self.first_branch}/revisions/{self.last_revision}/elements/{element_id}"
        element = self.session.get(get_element_url, verify=False).json()
        return element

    def post_element_body(self, element_id: str, element_body: dict):
        # post_element_url = f"{self.get_project_url}/branches/{self.first_branch}/revisions/{self.last_revision}/elements/{element_id}"
        pass
