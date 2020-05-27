from magic_twc_client import MagicClient
import json

FILE_NAME = "model_dict"


class MagicModel:
    def __init__(self, magic_client: MagicClient):
        self.magic_client = magic_client
        self.main_structure = {}
        self._init_main_structure()

    def get_first_structure_level(self, element_name: str):
        return self.main_structure[element_name]

    def change_element(self, element_name: str, ):
        pass

    def get_main_structure(self):
        return self.main_structure

    def _init_main_structure(self):
        # with open(FILE_NAME, 'r', encoding="utf8") as f:
        #     self.model_dict = json.load(f)
        #     return

        uml_model_id = self.magic_client.uml_model_id()
        uml_model = self.magic_client.get_element_body(uml_model_id)

        for unit in uml_model[1]["kerml:ownedElement"]:
            element_id = unit["@id"]
            element = self.magic_client.get_element_body(element_id)

            if "kerml:name" in element[1]:
                element_name = element[1]["kerml:name"]
                self.main_structure[element_name] = [element_id, element]

        # if self.model_dict:
        #     with open(FILE_NAME, 'w', encoding="utf8") as f:
        #         f.write(json.dumps(self.model_dict))

    def get_owned_elements(self, element: dict):
        element_structure = {}

        for unit in element[1]["kerml:ownedElement"]:
            unit_id = unit["@id"]
            unit = self.magic_client.get_element_body(unit_id)

            if "kerml:name" in unit[1]:
                unit_name = unit[1]["kerml:name"]
                if unit_name:
                    element_structure[unit_name] = [unit_id, unit]

        return element_structure
