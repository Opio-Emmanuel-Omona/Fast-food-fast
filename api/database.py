from flask import jsonify, request
import psycopg2
import jwt
import datetime


# app.config['SECRET_KEY'] = 'thisisthesecretkey'
# app.config['ADMIN_KEY'] = 'thisistheadminkey'


class DatabaseConnection():
    def __init__(self, value):
        if value:
            self.connection = psycopg2.connect(
                database="test_fast_food_fast_db",
                user="postgres",
                password="P@ss1234",
                host="127.0.0.1",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            print "Connected to test_fast_food_fast"
            self.drop_tables()
        else:
            self.connection = psycopg2.connect(
                database="fast_food_fast_db",
                user="postgres",
                password="P@ss1234",
                host="127.0.0.1",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            print "connected to fast_food_fast"

        self.create_user_table()
        self.create_order_table()
        self.create_menu_table()
        self.create_status_table()

    def create_user_table(self):
        sql = (
            '''CREATE TABLE IF NOT EXISTS "user" (
                username character varying(20) PRIMARY KEY,
                email character varying(50) NOT NULL,
                phone_no character varying(15) NOT NULL,
                password character varying(20) NOT NULL
            );'''
        )
        self.cursor.execute(sql)
        self.connection.commit()
        print ("User table create")

    def create_menu_table(self):
        sql = (
            '''
            CREATE TABLE IF NOT EXISTS "menu"(
                item_name character varying(20) PRIMARY KEY,
                price integer NOT NULL
            );
            '''
        )
        self.cursor.execute(sql)
        self.connection.commit()
        print ("Menu table create")

    def create_order_table(self):
        sql = (
            '''
            CREATE TABLE IF NOT EXISTS "order"(
                order_id SERIAL PRIMARY KEY,
                username character varying(20) NOT NULL,
                item_name character varying(20) NOT NULL,
                quantity integer NOT NULL,
                status character(15)
            )
            '''
        )
        self.cursor.execute(sql)
        self.connection.commit()
        print ("Order table create")

    def create_status_table(self):
        sql = (
            '''
            CREATE TABLE IF NOT EXISTS "status"(
                status_name character varying(15) PRIMARY KEY
            )
            '''
        )
        self.cursor.execute(sql)
        self.connection.commit()
        print ("Status table create")

    def create_user(self, user_dict):
        '''
        add user to table
        '''
        sql = "INSERT INTO \"user\"(username, email, phone_no, password) VALUES('"+user_dict['username']+"','"+user_dict['email']+"','"+user_dict['phone_no']+"','"+user_dict['password']+"');"
        self.cursor.execute(sql)
        self.connection.commit()

    def signin(self, user_dict):
        '''
        user logs in
        '''
        sql = "SELECT username, password FROM \"user\";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            if row[0] == user_dict['username'] and row[1] == user_dict['password']:
                # then login
                # give token based authentication to this user
                token = jwt.encode({
                    'username': user_dict['username'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    'thisisthesecretkey')
                self.connection.commit()
                return jsonify({'username': user_dict['username'], 'token': token})
        
        # ADMIN login
        if user_dict['username'] == 'admin' and user_dict['password'] == 'password':
            token = jwt.encode(
                {
                    'username': user_dict['username'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                'thisistheadminkey')
            self.connection.commit()
            print token
            return jsonify({'user': user_dict['username'], 'token': token})

        return jsonify({'answer': 401}), 401

    def add_order(self, user_dict):
        sql = "INSERT INTO \"order\" (username, item_name, quantity, status) VALUES('"+user_dict['username']+"','"+user_dict['item_name']+"','"+user_dict['quantity']+"', 'New');"
        self.cursor.execute(sql)
        self.connection.commit()

    def order_history(self, user_dict):
        sql = "SELECT username, item_name FROM \"order\";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # decdode the username from the token
        history = []
        for row in rows:
            if row[0] == user_dict['username']:  # username
                history.append({'item_name': row[1]})
        
        self.connection.commit()
        return history

    def add_menu(self, menu_dict):
        sql = "INSERT INTO \"menu\" (item_name, price) VALUES('"+menu_dict['item_name']+"', '"+menu_dict['price']+"');"
        self.cursor.execute(sql)
        self.connection.commit()

    def menu(self):
        sql = "SELECT * FROM \"menu\";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        menu = []
        for row in rows:
            item = {'item_name': row[0], 'price': row[1]}
            menu.append(item)
        self.connection.commit()
        return jsonify({'menu': menu})

    def fetch_all_orders(self):
        sql = "SELECT * FROM \"order\";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(
                {
                    'order_id': row[0],
                    'username': row[1],
                    'item_name': row[2],
                    'quantity': row[3],
                    'status': row[4]
                })
        self.connection.commit()
        return jsonify({'orders': orders})

    def fetch_specific_order(self, order_id):
        sql = "SELECT * FROM \"order\" WHERE order_id = '"+order_id+"';"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        order = []
        for row in rows:
            order.append(
                {
                    'order_id': row[0],
                    'username': row[1],
                    'item_name': row[2],
                    'quantity': row[3],
                    'status': row[4]
                })
        self.connection.commit()
        return jsonify({'order': order})

    def update_order_status(self, user_dict):
        if user_dict['order_id'] == '0':
            sql = "UPDATE \"order\" SET status = '"+user_dict['status_name']+"' WHERE username = '"+user_dict['username']+"' AND item_name = '"+user_dict['item_name']+"';"
            self.cursor.execute(sql)
            self.connection.commit()
        else:
            sql = "UPDATE \"order\" SET status = '"+user_dict['status_name']+"' WHERE order_id = '"+user_dict['order_id']+"';"
            self.cursor.execute(sql)
            self.connection.commit()

    def drop_tables(self):
        # First delete all the tests data
        sql1 = ('''DROP TABLE IF EXISTS "user";''')
        sql2 = ('''DROP TABLE IF EXISTS "order";''')
        sql3 = ('''DROP TABLE IF EXISTS "menu";''')
        self.cursor.execute(sql1)
        self.connection.commit()
        self.cursor.execute(sql2)
        self.connection.commit()
        self.cursor.execute(sql3)
        self.connection.commit()
