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


magic_client = MagicClient(username=username, pwd=password, twc_address=twc_address)
model = MagicModel(magic_client)

# main_structure[element_name] = [element_id, element]
model_structure = model.get_main_structure()

print("The main structure of the model:")
for key in model_structure.keys():
    print(key)

# let`s take


# magic_client.get_model_id()

# element_name = ""
# element = model.get_element(element_name)
# print(element)

# model.change_element(...)
