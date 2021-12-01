import ast
from level_1.communication_parser import CommunicationLogParser

def test_writing():
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')

    output_path = "./tests/test_output.json"
    processed_communication_sample = {
   'id':'testId',
   'telecom':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'category':'writer'
        }
    }
    communication_log_parser.communication_json_write(output_path, processed_communication_sample)

def test_read_json_output():
    input_path = "./tests/test_output.json"
    with open(input_path, 'r') as input_file:
        print(ast.literal_eval(' '.join(map(lambda s: s.replace('\n',''), input_file.readlines()))))


def test_should_rename_dict_keys():
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')
    communication_log_parser.config["keys_to_rename"]['telecom'] = 'communication_mean'
    communication_sample_before_renaming = {
   'id':'testId',
   'telecom':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'profession':'writer'
        }
    }

    expected_communication_sample = {
   'id':'testId',
   'communication_mean':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'category':'writer'
        }
    }

    assert(communication_log_parser.rename_keys(communication_sample_before_renaming) == expected_communication_sample)
    
def test_communication_parsing():
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')
    communication_sample = "id=testId|telecom=mail|created_at=1993-03-11 04:19:12|sender={'name': 'Kallum Wises', 'profession': 'writer'}"
    
    expected_communication_sample = {
   'id':'testId',
   'telecom':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'category':'writer'
        }
    }
    assert communication_log_parser.parse(communication_sample) == expected_communication_sample