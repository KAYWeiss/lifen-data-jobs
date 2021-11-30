from level_2.communications_db_io import MySQLCommunicationDB

def test_db_connect():
    my_config = {'user': 'root', 'password': 'new_password', 'host': 'localhost', 'database': 'lifen'}

    my_db = MySQLCommunicationDB(config = my_config)
    test_cursor = my_db.connector.cursor()
    query = ("SELECT * FROM communication ")
    test_cursor.execute(query)
    for elem in test_cursor:
        print(elem)
    my_db.close()
