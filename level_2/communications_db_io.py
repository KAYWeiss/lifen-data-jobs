from mysql import connector
import json
class MySQLCommunicationDB:

    def __init__(self, config):
        self.connector = connector.connect(**config)

    @classmethod
    def init_from_config_file(cls, config_file_path):
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            return cls(config)

    def close(self):
        self.connector.close()

        
    def create_communication_table(self):
        query = """CREATE TABLE communication(
            id varchar(100),
            telecom varchar(10),
            created_at timestamp,
            sender_name varchar(50),
            sender_category varchar(20)
            )"""
        create_cursor = self.connector.cursor()
        create_cursor.execute(query)

    def insert_one_communication(self, communication_log):
        db_com_log = (communication_log.get('id'),
        communication_log.get('telecom'),
        communication_log.get('created_at'),
        communication_log.get('sender').get('name'),
        communication_log.get('sender').get('category'),
        )
        query = """INSERT INTO communication 
               (id, telecom, created_at, sender_name, sender_category) 
               VALUES (%s, %s, %s, %s, %s)"""

        insert_cursor = self.connector.cursor()

        insert_cursor.execute(query, db_com_log)
