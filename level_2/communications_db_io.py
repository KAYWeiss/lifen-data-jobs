from mysql import connector
import json
import csv

class MySQLCommunicationDB:

    def __init__(self, config):
        self.connector = connector.connect(**config)

    @classmethod
    def init_from_config_file(cls, config_file_path):
        """ 
        This function initializes the DB from a config file path
        """
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            return cls(config)

    def close(self):
        """ 
        This function closes the connection
        """
        self.connector.close()

        
    def create_communication_table(self):
        """  
        This function creates the communication table
        """
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
        """  
        This function inserts a communication_log inside the communication table
        """
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

    def get_dematerialization_rate(self, output_file_path = None):
        """  
        This function queries the communication table to get the dematerialization rate
        for each liberal doctor. 
        It prints the results and saves them to a file if one is specified."""
        dematerilization_rate_cursor = self.connector.cursor()
        dematerilization_rate_query = """
        WITH liberal_doctors AS (SELECT sender_name, telecom, CASE WHEN telecom = 'paper' THEN 'True' END AS papered_com FROM communication WHERE sender_category = 'liberal')
        SELECT sender_name, (COUNT(papered_com) / COUNT(*)) AS dematerialization_rate FROM liberal_doctors GROUP BY sender_name
        """
        dematerilization_rate_cursor.execute(dematerilization_rate_query)
        results = dematerilization_rate_cursor.fetchall()

        if output_file_path is not None:
            with open(output_file_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(results)

    def get_doctors_list(self, output_file_path = None):
        """  
        This function queries the communication table to get the list of doctors that have done
        at least 5 communications following their first one.
        It prints the results and saves them to a file if one is specified.
        """
        seven_days_cursor = self.connector.cursor()
        seven_days_query = """
        WITH first_communication AS (SELECT sender_name, MIN(DATE_ADD(created_at, INTERVAL 7 DAY)) AS first_com_plus_7 
        FROM communication 
        GROUP BY sender_name),
        seven_days_communication AS (SELECT communication.sender_name, communication.id, created_at, first_com_plus_7 
        FROM communication JOIN first_communication
        ON communication.sender_name = first_communication.sender_name
        WHERE created_at <= first_com_plus_7)
        SELECT sender_name FROM seven_days_communication GROUP BY sender_name HAVING COUNT(*)>=5
        """

        seven_days_cursor.execute(seven_days_query)
        results = seven_days_cursor.fetchall()

        if output_file_path is not None:
            with open(output_file_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(results)