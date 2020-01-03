from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from DBConn import db_config
from psycopg2 import connect
from models.item import ItemModel

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',required=True, type=float, help='This field can not be  left black')

    ############################################
    #   GET METHOD                             #
    ############################################
    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json_format(), 200
        return {"message" : "item not found"}, 404

    ############################################
    #   POST METHOD                            #
    ############################################
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with  name {} already exists'.format(name)}, 400

        data = Items.parser.parse_args()
        item = ItemModel(name,data['price'])
        try:
            item.insert()
        except:
            return {"message": "An Exception occured"}
        return item.json_format(), 201

    ############################################
    #   DELETE METHOD                          #
    ############################################
    def delete(self, name):
        if ItemModel.find_by_name(name):
            item = ItemModel(name,None)
            try:
                item.delete()
                return {'message':'item deleted'}, 201
            except Exception as e:
                return {"message" : 'Error while deleting item :  {}'.format(e)}
        return {'message':'item {} does not existts'.format(name)}, 404

    ############################################
    #   PUT METHOD                          #
    ############################################
    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel(name,data['price'])
        if ItemModel.find_by_name(name):  
            item.update()
            return {'message':'item {} updated'.format(name)}, 200
        else:
            try:
               item.insert()
               return {'message':'item {} inserted'.format(name)}, 200
            except:
                return {'message' : "An Exception Happen" }
            return {'message':'item {} created'.format(name)}, 200


class ItemList(Resource):
    def get(self):
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        select_stmt  = "select item, price from public.items"
        cur.execute(select_stmt)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        items = []
        if rows:
            for row in rows:
                item =  {'item' : row[0], 'price':  row[1]}
                items.append(item)
            return {'items': items}, 200
        return {"message" : "item not found"}, 404

        