from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from DBConn import db_config
from psycopg2 import connect

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',required=True, type=float, help='This field can not be  left black')

    @jwt_required()
    def get(self, name):
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        select_stmt  = "select item, price from public.items where item = %s"
        cur.execute(select_stmt, (name,))
        row = cur.fetchone()
        conn.commit()
        conn.close()
        if row:
            return {'item' : row[0], 'price':  row[1]},200
        return {"message" : "item not found"}, 404
    
    @classmethod
    def find_by_name(cls, name):
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        select_stmt  = "select item, price from public.items where item = %s"
        cur.execute(select_stmt, (name,))
        row = cur.fetchone()
        conn.close()
        if row:
            return {'item' : row[0], 'price':  row[1]}


    def post(self, name):
        if self.find_by_name(name):
            return {'message': 'An item with  name {} already exists'.format(name)}, 400
        data = Items.parser.parse_args()
        item = {"item" : name, "price": data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An Exception occured"}
        return item, 201

    @classmethod
    def insert(cls, item):
        insert_stmt = "insert into public.items (item, price) values ( %s, %s)" 
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        cur.execute(insert_stmt, (item['item'],item['price']))
        conn.commit()
        conn.close()


    def delete(self, name):
        if self.find_by_name(name):
            delete_stmt = "delete from public.items where item = %s" 
            param = db_config('suppliers')
            conn = connect(**param)
            cur = conn.cursor()
            cur.execute(delete_stmt, (name,))
            conn.commit()
            conn.close()
            return {'message':'item deleted'}, 201
        return {'message':'item {} does not existts'.format(name)}, 404

    def put(self, name):
        data = Items.parser.parse_args()
        if self.find_by_name(name):
            update_stmt = "update  public.items set price = %s where item = %s" 
            param = db_config('suppliers')
            conn = connect(**param)
            cur = conn.cursor()
            cur.execute(update_stmt, (data['price'], name,))
            conn.commit()
            conn.close()
            return {'message':'item {} updated'.format(name)}, 200
        else:
            item = {"item":name,"price" : data['price']}
            try:
                self.insert(item)
            except:
                return {'message' : "An Exception Happen" }
            return {'message':'item {} created'.format(name)}, 200
            

        #data = Items.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price'    : data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item


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

        