import ast 
import json

class CommunicationLogParser:
    def __init__(self, cfg):
        self.config = cfg

    @classmethod
    def init_from_config_file(cls, config_file_path):
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            return cls(config)


    def parse(self, communication_log):
        """ 
        This function takes a string as input and transforms it to dict.
        It uses the input config to split the original string, and transform the different keys.
        """
        input_config = self.config.get('input')
        communication_log_informations = communication_log.split(input_config.get("log_separator"))
        communication_dict = {}
        for inf in communication_log_informations:
            k, v = inf.split(input_config.get("kv_separator"))
            if k in input_config.get('dict_keys'):
                v_dict = ast.literal_eval(v)
                communication_dict[k] = v_dict
            else:
                communication_dict[k] = v
        
        self.rename_keys(communication_dict)
        return communication_dict

    def communication_json_write(self, output_file_path, communication_log):
        """ 
        This function write a dict to a json file.
        It uses the config to define the indent, separatorsand quotes of the json output. 
        """
        output_config = self.config.get('output')
        output_string = json.dumps(communication_log, 
                indent = output_config.get('indent'), 
                separators = output_config.get('separators'))
        if output_config.get('double_quotes_to_single') == 'True':
            output_string = output_string.replace('\"', '\'')

        with open(output_file_path, 'w') as output_file:
            output_file.writelines(output_string)

    
    def rename_keys(self, dict_to_change):
        """ 
        This function takes as 2 strings and a dict and returns a new dict with a key renamed
        """
        changed_dict = dict_to_change
        for old_key, new_key in self.config.get('keys_to_rename').items():
            nested_dict = changed_dict
            for nested_key in old_key.split('.')[:-1]:
                nested_dict = nested_dict.get(nested_key)
            nested_dict[new_key] = nested_dict.pop(old_key.split('.')[-1])
        return changed_dict


    def communication_file_read(input_file_path):
        """ 
        This function opens a file andread and returns the first line as a string.
        """
        with open(input_file_path,'r') as input_file:
            return input_file.readline()

