import sys
from model_data import username, password, twc_address
from magic_twc_client import MagicClient
from magic_model import MagicModel

# based on this example
# https://docs.nomagic.com/plugins/servlet/mobile?contentId=38050235#content/view/38050235

# suppress useless warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


def print_structure(element_name: str, element_structure: dict):
    print(f"The structure of the {element_name}:")
    for key in element_structure.keys():
        print(key)
    print("---------------------------------- \n")


magic_client = MagicClient(username=username, pwd=password, twc_address=twc_address)
model = MagicModel(magic_client)

model_structure = model.get_main_structure()
# -> main_structure[element_name] = [element_id, element]

print_structure("the model", model_structure)

# let`s take "6 - Верификация требований" element
element_6_name = "6 - Верификация требований"
element_6 = model_structure[element_6_name][1]
element_6_structure = model.get_owned_elements(element_6)
# -> structure[element_name] = [element_id, element]

print_structure(element_6_name, element_6_structure)
