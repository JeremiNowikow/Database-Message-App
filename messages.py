import argparse
from clcrypto import check_password
from models import User, Message
from psycopg2 import connect, OperationalError

USER = "postgres"
PASSWORD = "coderslab"
HOST = "localhost"
DB_NAME = "message_app_db"

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min. 8 characters)")
parser.add_argument("-s", "--send", help="text of the message to send")
parser.add_argument("-l", "--list", help="lists all messages", action="store_true")
parser.add_argument("-t", "--to", help="name of the recipient of the message")

args = parser.parse_args()


# prints out all the messages received by the user
def list_user_messages(curs, user):
    messages = Message.load_all_messages(curs, user.id)
    for message in messages:
        sender = User.load_user_by_id(curs, message.from_id)
        print(20*"*")
        print(sender.username)
        print(message.creation_date)
        print(message.text)
        print(20 * "*")


# adds new message to the database, with specified text and recipient
def send_message(curs, text, sender, recipient_name):
    if len(text) > 255:
        print("The message is too short.")
        return
    recipient = User.load_user_by_username(curs, recipient_name)
    if recipient:
        message = Message(sender.id, recipient.id, text)
        message.save_to_db(curs)
        print("Message sent")
    else:
        print("No such user exists")


if __name__ == "__main__":
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, port=5432, database=DB_NAME)
        cnx.autocommit = True
        cursor = cnx.cursor()

        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    list_user_messages(cursor, user)
                elif args.send and args.to:
                    send_message(cursor, args.send, user, args.to)
                else:
                    parser.print_help()
            else:
                print("Invalid user or incorrect password")
        else:
            parser.print_help()

        cnx.close()

    except OperationalError as error:
        print(error)

    
