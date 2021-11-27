import ast
from level_1.communication_parser import parse, communication_json_write

def test_communication():
    communication_sample = "id=testId|telecom=mail|created_at=1993-03-11 04:19:12|sender={'name': 'Kallum Wises', 'profession': 'writer'}"
    
    processed_communication_sample = {
   'id':'testId',
   'telecom':'mail',
   'created_at':'1993-03-11 04:19:12',
   'sender':{
      'name':'Kallum Wises',
      'category':'writer'
        }
    }
    assert parse(communication_sample) == processed_communication_sample

def test_writing():
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
    communication_json_write(output_path, processed_communication_sample)

def test_read_json_output():
    input_path = "./tests/test_output.json"
    with open(input_path, 'r') as input_file:
        print(ast.literal_eval(' '.join(map(lambda s: s.replace('\n',''), input_file.readlines()))))