from psycopg2 import connect
from DBConn import db_config

class ItemModel:
    def __init__(self, item, price):
        self.item = item
        self .price = price
    
    def json_format(self):
        return {'item' : self.item, 'price' : self.price}

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
            return cls(*row)
          
    def insert(self):
        insert_stmt = "insert into public.items (item, price) values ( %s, %s)" 
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        cur.execute(insert_stmt, (self.item,self.price))
        conn.commit()
        conn.close()

    def update(self):
        update_stmt = "update  public.items set price = %s where item = %s" 
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        cur.execute(update_stmt, (self.price, self.item,))
        conn.commit()
        conn.close()

    def delete(self):
        delete_stmt = "delete from public.items where item = %s" 
        param = db_config('suppliers')
        conn = connect(**param)
        cur = conn.cursor()
        cur.execute(delete_stmt, (self.item,))
        conn.commit()
        conn.close()