from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

USER = "postgres"
HOST = "localhost"
PASSWORD = "password"


def create_db(db_name):
    """
    Create database named parm db_name using psycopg2.

    :param str db_name: name of database,

    :rtype:
    :return:
    """

    sql_crate_db = f"CREATE DATABASE {db_name};"

    sql_crate_tables = [f"""CREATE TABLE users (
                        id serial,
                        username varchar(255) UNIQUE,
                        hashed_password varchar(80),
                        PRIMARY KEY(id)
                    );""",

                    f"""CREATE TABLE messages (
                        id serial,
                        from_id int REFERENCES users(id) ON DELETE CASCADE NOT NULL,
                        to_id int REFERENCES users(id) ON DELETE CASCADE NOT NULL,
                        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        text varchar(255),
                        PRIMARY KEY(id)
                        );"""
                    ]

    try:
        # connect to DB server and create database
        cnx = connect(user=USER, password=PASSWORD, host=HOST)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_crate_db)
        print(f"Database {db_name} has been created.")

        # connect to the crated DB and crate TABLES
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        for i, sql_query in enumerate(sql_crate_tables):
            cursor.execute(sql_query)
            print(f"Table {i} for {db_name} has been created.")

    except OperationalError:
        print("Error !")
    except DuplicateDatabase as error:
        print(error)
    except DuplicateTable as error:
        print(error)

    else:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    create_db('test')


