import argparse
from psycopg2.errors import UniqueViolation
from psycopg2 import connect, OperationalError

from clcrypto import check_password
from models import User

USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
DB_NAME = "message_app_db"

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min. 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min. 8 characters)")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
parser.add_argument("-l", "--list", help="lists all users", action="store_true")
parser.add_argument("-d", "--delete", help="deletes user", action="store_true")

args = parser.parse_args()


# adds a new user with the specified username and password to the database
def add_user(curs, username, password):
    if len(password) < 8:
        print("This password is too short. Minimum length: 8 characters")
        return
    try:
        user = User(username, password)
        user.save_to_db(curs)
        print("User has been created")
    except UniqueViolation:
        print("This user already exists")


# changes the password of the given user, if the inputted password is correct
def edit_user(curs, username, password, new_password):
    user = User.load_user_by_username(curs, username)
    if not user:
        print("User does not exist")
        return
    if check_password(password, user.hashed_password):
        if len(new_password) < 8:
            print("This password is too short. Minimum length: 8 characters")
            return
        user.hashed_password = new_password
        user.save_to_db(curs)
    else:
        print("Incorrect password.")


# deletes the user with the specified username from the database
def delete_user(curs, username, password):
    user = User.load_user_by_username(curs, username)
    if not user:
        print("User does not exist")
        return
    if check_password(password, user.hashed_password):
        user.delete(curs)
        print("User deleted")
    else:
        print("Incorrect password")


# lists all current users from the database
def list_users(curs):
    users = User.load_all_users(curs)
    for user in users:
        print(f"{user.id}. {user.username}")


if __name__ == "__main__":
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, port=5432, database=DB_NAME)
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.new_pass and args.edit:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            add_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()

        cnx.close()
    except OperationalError as error:
        print(error)
