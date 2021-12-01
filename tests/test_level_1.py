import ast
import pytest
from level_1.communication_parser import CommunicationLogParser

@pytest.fixture
def expected_result():
    return {
   'id':'testId',
   'telecom':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'category':'writer'
        }
    }
    
def test_writing(expected_result):
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')

    output_path = "./tests/test_output.json"

    communication_log_parser.communication_json_write(output_path, expected_result)

def test_read_json_output():
    input_path = "./tests/test_output.json"
    with open(input_path, 'r') as input_file:
        print(ast.literal_eval(' '.join(map(lambda s: s.replace('\n',''), input_file.readlines()))))


def test_should_rename_dict_keys(expected_result):
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')
    communication_log_parser.config["keys_to_rename"]['communication_mean'] = 'telecom'
    communication_sample_before_renaming = {
   'id':'testId',
   'communication_mean':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'profession':'writer'
        }
    }

    assert(communication_log_parser.rename_keys(communication_sample_before_renaming) == expected_result)
    
def test_communication_parsing(expected_result):
    communication_log_parser = CommunicationLogParser.init_from_config_file('./level_1/communication_config.json')
    communication_sample = "id=testId|telecom=mail|created_at=1993-03-11 04:19:12|sender={'name': 'Kallum Wises', 'profession': 'writer'}"
    
    assert(communication_log_parser.parse(communication_sample) == expected_result)