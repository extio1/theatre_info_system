from sys import argv
from config import config
from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
            host=config['host'],
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database=config['database']
    ) as connection:
        with connection.cursor() as cursor:
            with open("./script/sample/"+argv[1]+".sql", "r") as f:
                for insert_table_query in f.read().split(';'):
                    if len(insert_table_query) > len("INSERT"):
                        print(insert_table_query)
                        cursor.execute(insert_table_query)
            connection.commit()

        print("Success")
except Error as e:
    print(e)
