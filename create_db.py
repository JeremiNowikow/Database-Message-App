from psycopg2 import connect, sql, OperationalError, DatabaseError

from models import User, Message

USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
DB_NAME = "message_app_db"

try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST, port=5432, database=DB_NAME)
    cnx.autocommit = True
    cursor = cnx.cursor()
    print("Connected")
except OperationalError as error:
    print("Connection error")
    raise ValueError(f"Connection error: {error}")

query_create_database = sql.SQL("""
    CREATE DATABASE message_app_db;
""")

query_create_users_table = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name}(
        ID SERIAL PRIMARY KEY,
        username VARCHAR(255),
        hashed_password VARCHAR(80)
        
    )
""").format(table_name=sql.Identifier('Users'))

query_create_messages_table = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table_name}(
        ID SERIAL,
        from_id INTEGER,
        to_id INTEGER,
        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        text VARCHAR(255),
        FOREIGN KEY (from_id) REFERENCES {foreign_table_name}(ID),
        FOREIGN KEY (to_id) REFERENCES {foreign_table_name}(ID)
    )
""").format(table_name=sql.Identifier('Messages'), foreign_table_name=sql.Identifier('Users'))


try:
    cursor.execute(query_create_database)
    print("Created a database")
except DatabaseError as error:
    print("Database already exists")

try:
    cursor.execute(query_create_users_table)
    print("Users table created")
    cursor.execute(query_create_messages_table)
    print("Messages table created")
except DatabaseError as error:
    print(error)

cnx.close()

