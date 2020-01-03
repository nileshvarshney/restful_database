from psycopg2 import connect
from DBConn import db_config

class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id,
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        print(username)
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        query  = "select * from public.users where username = %s"
        cur.execute(query, (username,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user  = None
        conn.close()
        return  user
        

    @classmethod
    def find_by_id(cls, _id):
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        query  = "select * from public.users where id = %s"
        result = cur.execute(query, (_id,))
        row = cur.fetchone()
        if row:
            user = cls(*row)
        else:
            user  = None
        conn.close()
        return user


