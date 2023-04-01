from clcrypto import password_hash


class User:
    def __init__(self, username="", password="", salt=""):

        self._id = -1

        self.username = username

        self._hashed_password = password_hash(password, salt)

    @property
    def id(self):

        return self._id

    @property
    def hashed_password(self):

        return self._hashed_password

    # uses the password_hash method from clcrypto.py to generate a hashed user password
    def set_password(self, password, salt=""):

        self._hashed_password = password_hash(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):

        self.set_password(password)

    # saves the object of User class to the table Users in database
    def save_to_db(self, cursor):

        if self._id == -1:

            sql = """INSERT INTO "Users"(username, hashed_password)

                            VALUES(%s, %s) RETURNING id"""

            values = (self.username, self.hashed_password)

            cursor.execute(sql, values)

            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']

            return True

        else:

            sql = """UPDATE "Users" SET username=%s, hashed_password=%s

                           WHERE id=%s"""

            values = (self.username, self.hashed_password, self.id)

            cursor.execute(sql, values)

            return True

    # loads the user possessing the given ID
    @staticmethod
    def load_user_by_id(cursor, id_):

        sql = """SELECT id, username, hashed_password FROM "Users" WHERE id=%s"""

        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple

        data = cursor.fetchone()

        if data:

            id_, username, hashed_password = data

            loaded_user = User(username)

            loaded_user._id = id_

            loaded_user._hashed_password = hashed_password

            return loaded_user

    # loads the first user possessing the given username
    @staticmethod
    def load_user_by_username(cursor, username_):
        sql = """SELECT id, username, hashed_password FROM "Users" WHERE username=%s"""

        cursor.execute(sql, (username_,))  # (id_, ) - cause we need a tuple

        data = cursor.fetchone()

        if data:

            id_, username, hashed_password = data

            loaded_user = User(username)

            loaded_user._id = id_

            loaded_user._hashed_password = hashed_password

            return loaded_user

    # loads all rows from the database Users and saves them as a list of User objects
    @staticmethod
    def load_all_users(cursor):

        sql = """SELECT id, username, hashed_password FROM "Users" """

        users = []

        cursor.execute(sql)

        for row in cursor.fetchall():

            id_, username, hashed_password = row

            loaded_user = User()

            loaded_user._id = id_

            loaded_user.username = username

            loaded_user._hashed_password = hashed_password

            users.append(loaded_user)

        return users

    # deletes the User object and the row in the database that possesses the same id
    def delete(self, cursor):

        sql = """DELETE FROM "Users" WHERE id=%s"""

        cursor.execute(sql, (self.id,))

        self._id = -1

        return True


class Message:
    def __init__(self, from_id="", to_id="", text=""):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None

    @property
    def id(self):
        return self._id

    # Saves a message to the database
    def save_to_db(self, cursor):
        if self._id == -1:

            sql = """INSERT INTO "Messages"(from_id, to_id, text)

                            VALUES(%s, %s, %s) RETURNING id, creation_date"""

            values = (self.from_id, self.to_id, self.text)

            cursor.execute(sql, values)

            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']

            return True

        else:

            sql = """UPDATE "Messages" SET from_id=%s, to_id=%s, text=%s

                           WHERE id=%s"""

            values = (self.from_id, self.to_id, self.text, self.id)

            cursor.execute(sql, values)

            return True

    # returns a list of all messages from the database as objects of the Message class
    @staticmethod
    def load_all_messages(cursor, user_id=None):
        if user_id:
            sql = """SELECT id, from_id, to_id, creation_date, text FROM "Messages" WHERE to_id=%s """
            cursor.execute(sql, (user_id,))
        else:
            sql = """SELECT id, from_id, to_id, creation_date, text FROM "Messages" """
            cursor.execute(sql)

        messages = []


        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row

            loaded_message = Message()

            loaded_message._id = id_
            loaded_message.from_id = from_id
            loaded_message.to_id = to_id
            loaded_message.creation_date = creation_date
            loaded_message.text = text

            messages.append(loaded_message)


        return messages
