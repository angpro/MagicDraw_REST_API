import sys
from model_data import username, password, twc_address

# based on this example
# https://docs.nomagic.com/plugins/servlet/mobile?contentId=38050235#content/view/38050235

# class MagicClient for:
# -- communication with TWC
# -- get ID of main UPL model of the project
from magic_twc_client import MagicClient

# class MagicModel for:
# -- manipulation with elements of the project
from magic_model import MagicModel

# suppress useless warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


# print element names of the structure
def print_structure(element_name: str, element_structure: dict):
    print(f"The structure of the {element_name}:")
    if element_structure:
        for key in element_structure.keys():
            print(key)
        print("---------------------------------- \n")
    else:
        print("...it is empty!")
        print("---------------------------------- \n")


def main():
    magic_client = MagicClient(username=username, pwd=password, twc_address=twc_address)
    model = MagicModel(magic_client)

    # get main structure of "Swarm CubeSat" project, it is a dictionary:
    # -> main_structure[element_name] = [element_id, element_json]
    model_structure = model.get_main_structure()

    # let's print element names of the main structure of "Swarm CubeSat" project
    # to check what element names we have to continue go deeper into the project
    print_structure("the model", model_structure)

    # ---- 1 LEVEL -----
    # let`s take "Test_folder" element
    element1_name = "Test_folder"
    element1 = model_structure[element1_name][1]
    # -> element_structure[element_name] = [element_id, element_json]
    element1_structure = model.get_owned_elements(element1)
    # -> structure[element_name] = [element_id, element]

    # let's print element names of the structure of chosen element
    print("---- 1 LEVEL -----")
    print_structure(element1_name, element1_structure)

    # ----- 2 LEVEL -----
    # let's take "New_test" from chosen element, and look what is into
    element2_name = "New_test"
    element2 = element1_structure[element2_name][1]
    # -> element_structure[element_name] = [element_id, element_json]
    element2_structure = model.get_owned_elements(element2)
    print("---- 2 LEVEL -----")
    print_structure(element2_name, element2_structure)

    # ----- 3 LEVEL -----
    # let's take "value" from chosen element, and look what is into
    element3_name = "value"
    element3 = element2_structure[element3_name][1]
    # -> element_structure[element_name] = [element_id, element_json]
    element3_structure = model.get_owned_elements(element3)
    print("---- 3 LEVEL -----")
    print_structure(element3_name, element3_structure)

    # ----- CHANGE THE ELEMENT -----

    # STEP 1
    # print body of the element which we want to change
    print("The element ID which we what to change:")
    print(element2_structure[element3_name][0])  # ID of the element
    print("\n")
    element_to_change = element2_structure[element3_name][1]

    # STEP 2
    # determine what field we want to change, in our case it is "defaultValue"
    # and get field "defaultValue" (it is element) by it`s ID
    field_to_change_element_id = element_to_change[1]["kerml:esiData"]["defaultValue"]["@id"]
    print("The element field ID what we want to change:")
    print(field_to_change_element_id)
    print("\n")
    field_to_change_element = magic_client.get_element_body(field_to_change_element_id)

    # STEP 3
    # look into field what we want to change, find the value we want to change
    print("State of the field what we want to change")
    print("value: ", field_to_change_element[1]["kerml:esiData"]["value"])
    print("The element what we want to change with new value:")
    print(field_to_change_element_id)
    print(field_to_change_element)
    print("\n")

    # STEP 4
    # new_value = "3"
    new_value = '3'
    print("New value is: ", new_value)
    print("\n")

    # prepare element field with new value to POST
    uml_Package = model.uml_Package_url

    ## URL to post new value
    ## https://10.30.254.66:8111/osmc/workspaces/4d6ce495-1273-452c-a548-36fcd922184e/resources/04deb4d0-a511-49a7-99a4-a25a6055e88d/elements/4dda3683-01e8-4e41-924c-3bae2325f4d8

    # uml_Package = "https://10.30.254.66:8111/osmc/schema/uml/2014345/Package"
    # base = "https://10.30.254.66:8111/osmc/workspaces/4d6ce495-1273-452c-a548-36fcd922184e/resources/04deb4d0-a511-49a7-99a4-a25a6055e88d/branches/1db29c03-caf0-46f9-b15a-79565c8e54ba/revisions/4/elements"
    # kerml = "https://10.30.254.66:8111/osmc/schema/kerml/20140325"
    # field_to_change_element_id = "4dda3683-01e8-4e41-924c-3bae2325f4d8"

    # updated_field = {
    #         "@context": {
    #             "@base": base,  # field_to_change_element[1]["@base"],
    #             "kerml": kerml,  # field_to_change_element[1]["@context"]["kerml"],
    #             "uml:Package": uml_Package
    #         },
    #         "kerml:esiData": {
    #             "value": new_value
    #         }
    #     }

    updated_field = {
            "@context": {
                "@base": field_to_change_element[1]["@base"],
                "kerml": field_to_change_element[1]["@context"]["kerml"],
                "uml:Package": uml_Package
            },
            "kerml:esiData": {
                "value": new_value
            }
        }

    # STEP 5
    # finally post new value of the element field
    print("Parameters to PUT:")
    magic_client.put_element_body(element_id=field_to_change_element_id, element_body=updated_field)


if __name__ == '__main__':
    main()
