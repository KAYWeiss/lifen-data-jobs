from os import listdir, makedirs, path
import time
from level_1.communication_parser import CommunicationLogParser
from level_2.communications_db_io import MySQLCommunicationDB

communication_log_parser = CommunicationLogParser.init_from_config_file('level_1/communication_config.json')    

mysql_db = MySQLCommunicationDB.init_from_config_file('level_2/mysql_db_config.json')
mysql_db.create_communication_table()

for input_file_path in listdir('communications'):
    output_name = f"./processed/{input_file_path}"

    # Parsing the logs

    processed_communication_log = communication_log_parser.parse(
            CommunicationLogParser.communication_file_read(f"communications/{input_file_path}"))

    # level_1 : saving the file as a json

    makedirs(path.dirname(output_name), exist_ok=True)

    processed_log = communication_log_parser.communication_json_write(
        output_name, 
        processed_communication_log)
    
    # level_2 : saving it in a MySQL DB 
    mysql_db.insert_one_communication(processed_communication_log)

mysql_db.close()

