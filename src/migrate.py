from config import config
from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
            host=config['host'],
            user=input("Enter username: "),
            password=getpass("Enter password: "),
    ) as connection:  # Connection with User-Password enter
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS "+config["database"])
            cursor.execute("CREATE DATABASE "+config["database"])
            cursor.execute("USE "+config["database"])

            with open("./script/migrate/migrate.sql", "r") as f:
                for create_table_query in f.read().split(';'):
                    print(create_table_query)
                    if len(create_table_query) > len("CREATE"):
                        cursor.execute(create_table_query)
                        connection.commit()

        print("Success")
except Error as e:
    print(e)
