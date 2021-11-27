import ast 
import json


def parse(communication_log):
    """ 
    This function takes a string as input and transforms it to dict
    """
    communication_log_informations = communication_log.split("|")
    communication_dict = {}
    for inf in communication_log_informations:
        k, v = inf.split("=")
        if k == 'sender':
            v_dict = ast.literal_eval(v)
            rename_key('profession', 'category', v_dict)
            communication_dict[k] = v_dict
        else:
            communication_dict[k] = v
    return communication_dict

def rename_key(old_name, new_name, dict_to_change):
    """ 
    This function takes as 2 strings and a dict and returns a new dict with a key renamed
    """
    if old_name in dict_to_change.keys():
        dict_to_change[new_name] = dict_to_change.pop(old_name)
    else:
        dict_to_change

def communication_file_read(input_file_path):
    """ 
    This function opens a file andread and returns the first line as a string.
    """
    with open(input_file_path,'r') as input_file:
        return input_file.readline()

def communication_json_write(output_file_path, communication_log):
    """ 
    This function write a dict to a json file
    """
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(
            json.dumps(communication_log, indent = 4, separators=(',',':'))
                .replace('\"', '\'')
        )

