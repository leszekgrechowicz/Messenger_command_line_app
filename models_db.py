from crypt_pass import hash_password


class User:
    def __init__(self, username="", password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self, cursor):

        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_name(cursor, name):

        sql = "SELECT id, username, hashed_password FROM users WHERE username LIKE %s"
        cursor.execute(sql, (name,))  # (name, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):

        sql = f"SELECT id, username, hashed_password FROM users WHERE id={id_}"
        cursor.execute(sql)
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user


    @staticmethod
    def load_all_users(cursor):

        sql = "SELECT id, username, hashed_password FROM Users"
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

    def delete(self, cursor):
        """Deletes User by id"""
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:

    def __init__(self, sender_id=None, receiver_id=None, message_='', creation_date=None):

        self._id = -1
        self.from_id = sender_id
        self.to_id = receiver_id
        self.text = message_
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def save_to_db(self, cursor):
        """Saves changes to the DataBase"""

        if self._id == -1:
            sql = """INSERT INTO messages (from_id, to_id, text)
                            VALUES(%s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self._id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor, user_id):
        """Draws all messages from the DataBase"""

        sql = f"SELECT id, from_id, to_id, creation_date, text FROM messages WHERE to_id={user_id} OR from_id={user_id};"

        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_user = Message(from_id, to_id, text, creation_date)
            loaded_user._id = id_

            messages.append(loaded_user)
        return messages

    @staticmethod
    def load_new_messages(cursor, user_id):
        """Draws all new messages from the DataBase"""

        sql = f"SELECT id, from_id, to_id, creation_date, text FROM messages WHERE to_id={user_id} AND is_read IS FALSE;"

        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_user = Message(from_id, to_id, text, creation_date)
            loaded_user._id = id_

            messages.append(loaded_user)
        return messages
