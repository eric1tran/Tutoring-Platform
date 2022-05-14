from mysql.connector import connect
import hashlib

class MySqlDBConnection(object):
    def __init__(self, host, user, password, database):
        self.session = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def __enter__(self):
        self.session = connect(host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


def hash_password(password):
    if not password or not isinstance(password, str):
        return None

    return hashlib.sha256(password.encode('utf-8')).hexdigest()