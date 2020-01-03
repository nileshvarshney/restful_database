from flask_restful import reqparse, Resource
from psycopg2 import connect
from DBConn import db_config
from user import User

class  RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(name='username', required=True, type=str, help='username can not be left black')
    parser.add_argument(name='password', required=True, type=str, help='password can not be left black')

    def post(self):
        data = RegisterUser.parser.parse_args()
        if User.find_by_username(data['username']):
            return {"message" : "User already exists"}, 400

        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        insert_stmt  = "insert  into public.users (username, password) values (%s, %s)"
        cur.execute(insert_stmt, (data['username'], data['password'],))
        conn.commit()
        conn.close()
        return {"message":"User created successfully"}, 201

