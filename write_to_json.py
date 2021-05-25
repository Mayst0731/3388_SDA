import json


def write_to_json(lst,file_name):
    with open(file_name, 'w') as cp:
        json.dump(lst, cp,indent=4)