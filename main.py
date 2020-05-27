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
    if element_structure.keys():
        for key in element_structure.keys():
            print(key)
        print("---------------------------------- \n")
    else:
        print("...it is empty!")
        print(element_structure)
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

    # 1 LEVEL
    # let`s take "ПАПКА ДЛЯ АНГЕЛИНЫ" element
    element1_name = "ПАПКА ДЛЯ АНГЕЛИНЫ"
    element1 = model_structure[element1_name][1]
    element1_structure = model.get_owned_elements(element1)
    # -> structure[element_name] = [element_id, element]

    # let's print element names of the structure of chosen element
    print_structure(element1_name, element1_structure)

    # 2 LEVEL
    # let's take "SOME_ELEMENT" from chosen element, and look what is into
    element2_name = "SOME_ELEMENT"
    element2 = element1_structure[element2_name][1]
    element2_structure = model.get_owned_elements(element2)
    print_structure(element2_name, element2_structure)

    # 3 LEVEL
    # let's take "SOME_VALUE" from chosen element, and look what is into
    element3_name = "SOME_VALUE"
    element3 = element2_structure[element3_name][1]
    element3_structure = model.get_owned_elements(element3)
    print_structure(element3_name, element3_structure)

    # print body of the element which we want to change
    print("Body of the element which we want to change")
    print(element3)

    # let's chech


if __name__ == '__main__':
    main()
