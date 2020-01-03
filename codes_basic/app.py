from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
from user import RegisterUser
from item import ItemList, Items

app = Flask(__name__)
api = Api(app)
app.secret_key='sanjose'
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)  # /auth

api.add_resource(Items,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(RegisterUser,'/registerUser')

if __name__ == "__main__":
    app.run(port=5000,debug=True)