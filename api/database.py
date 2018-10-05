import psycopg2
import jwt
import os
import datetime


class DatabaseConnection():
    def __init__(self):
        # Data = "test_fast_food_fast_db"
        # User = "postgres"
        # Password = "P@ss1234"
        # Host = "127.0.0.1"

        # if os.getenv('env') == "testing":
        Data = "d64v4cgifl4omb",
        User = "zpfghsehqzbqjr",
        Password = "b578a4e87c4e9e0073e825046b92630084e354e09118345736d9eca32e24c4a6",
        Host = "ec2-54-83-50-145.compute-1.amazonaws.com"

        self.connection = psycopg2.connect(
            database=Data,
            user=User,
            password=Password,
            host=Host,
            port="5432"
        )
        self.cursor = self.connection.cursor()
        print ("Connected to test_fast_food_fast")
    
    def setuptables(self):
        self.create_user_table()
        self.create_status_table()
        self.create_order_table()
        self.create_menu_table()

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
        print ("User table created")

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
        sql0 = (
            '''
            DROP TABLE status
            '''
        )
        self.cursor.execute(sql0)
        self.connection.commit()
        print ("Status table populated")

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

        sql1 = (
            '''
            INSERT INTO "status"(status_name)
            VALUES('New'), ('Processing'), ('Cancelled'), ('Completed')
            '''
        )
        self.cursor.execute(sql1)
        self.connection.commit()
        print ("Status table populated")

    def create_user(self, user_dict):
        '''
        add user to table
        '''
        sql = (
            '''
            SELECT username, email from "user";
            '''
        )
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        for row in rows:
            if row[0] == user_dict['username']:
                return {'message': 'username already taken',
                        'status': False}
            if row[1] == user_dict['email']:
                return {'message': 'email already taken',
                        'status': False}
        sql = (
            '''
            INSERT INTO "user"(username, email, phone_no, password)
            VALUES(%s, %s, %s, %s)
            '''
        )
        self.cursor.execute(sql, [
                                    user_dict['username'],
                                    user_dict['email'],
                                    user_dict['phone_no'],
                                    user_dict['password']])
        self.connection.commit()
        return {'message': user_dict['username'] + ' created succesfully',
                'status': True}

    def signin(self, user_dict):
        '''
        user logs in
        '''
        sql = "SELECT username, password FROM \"user\";"
        self.cursor.execute(sql)
        self.connection.commit()
        rows = self.cursor.fetchall()
        print("Before row")
        for row in rows:
            print("Afyer row")
            if row[0] == user_dict['username'] and row[1] == user_dict['password']:
                # then login
                # give token based authentication to this user
                token = jwt.encode({
                    'username': user_dict['username'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    'qwertyuiopasdfghjkl')
                return {'username': user_dict['username'],
                        'token': token,
                        'status': True}
        
        # ADMIN login
        if user_dict['username'] == 'admin' and user_dict['password'] == 'password':
            token = jwt.encode(
                {
                    'username': user_dict['username'],
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                },
                'lkjhgfdsapoiuytrewq')
            self.connection.commit()
            print(token)
            return {'username': user_dict['username'],
                    'token': token,
                    'status': True}

        return {'message': 'The username and password do not exist',
                'status': False}

    def add_order(self, user_dict):
        sql = (
            '''
            SELECT * FROM "menu" WHERE item_name = %s;
            '''
        )
        self.cursor.execute(sql, [user_dict['item_name']])
        rows = self.cursor.fetchall()
        self.connection.commit()
        if rows:
            sql = (
                '''
                SELECT * FROM "order" WHERE username = %s AND item_name = %s;
                '''
            )
            self.cursor.execute(sql, [user_dict['username'], user_dict['item_name']])
            rows = self.cursor.fetchall()
            self.connection.commit()
            if not rows:
                sql = (
                    '''
                    INSERT INTO "order"(username, item_name, quantity, status)
                    VALUES(%s, %s, %s, 'New');
                    '''
                )
                self.cursor.execute(sql, [
                                            user_dict['username'],
                                            user_dict['item_name'],
                                            user_dict['quantity']
                                        ])
                self.connection.commit()
                return {'message': 'Order has been placed', 'status': True}
            return {'message': 'Order already exists', 'status': False}
        return {'message': 'Order item not in menu', 'status': False}

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
        # First check if the item is already in the menu
        sql = (
            '''
            SELECT * FROM "menu" WHERE item_name = %s;
            '''
        )
        self.cursor.execute(sql, [menu_dict['item_name']])
        rows = self.cursor.fetchall()
        self.connection.commit()
        if rows:
            return {'message': 'Item already in menu',
                    'status': False}
        sql = (
            '''
            INSERT INTO "menu"(item_name, price)
            VALUES(%s, %s);
            '''
        )
        self.cursor.execute(sql, [menu_dict['item_name'], menu_dict['price']])
        self.connection.commit()
        return {'message': 'item succesfully added to menu', 'status': True}

    def menu(self):
        sql = "SELECT * FROM \"menu\";"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        menu = []
        for row in rows:
            item = {'item_name': row[0], 'price': row[1]}
            menu.append(item)
        self.connection.commit()
        return {'menu': menu}

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
        return {'orders': orders}

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
        return {'order': order}

    def update_order_status(self, user_dict):
        if user_dict['order_id'] == '0':
            sql = (
                '''
                UPDATE "order" SET status = %s WHERE username = %s AND item_name = %s;
                '''
            )
            self.cursor.execute(sql, [user_dict['status_name'], user_dict['username'], user_dict['item_name']])
            self.connection.commit()
        else:
            sql = (
                '''
                SELECT * FROM "order" WHERE order_id = %s;
                '''
            )
            self.cursor.execute(sql, [user_dict['order_id']])
            rows = self.cursor.fetchall()
            self.connection.commit()
            if rows:
                # check for the status
                sql = (
                    '''
                    SELECT * FROM "status" WHERE status_name = %s;
                    '''
                )
                self.cursor.execute(sql, [user_dict['status_name']])
                rows = self.cursor.fetchall()
                self.connection.commit()
                if rows:
                    sql = (
                        '''
                        UPDATE "order" SET status = %s WHERE order_id = %s;
                        '''
                    )
                    self.cursor.execute(sql)
                    self.connection.commit() 
                else:       
                    return {'message': 'wrong status provided', 'status': False}
            else:
                return {'message': 'Order doesn\'t exist', 'status': False}
        return {'message': 'Order status succefully updated', 'status': True}   

    def drop_tables(self):
        # First delete all the tests data
        sql1 = ('''DROP TABLE IF EXISTS "user";''')
        sql2 = ('''DROP TABLE IF EXISTS "order";''')
        sql3 = ('''DROP TABLE IF EXISTS "menu";''')
        sql4 = ('''DROP TABLE IF EXISTS "status";''')
        self.cursor.execute(sql1)
        self.connection.commit()
        self.cursor.execute(sql2)
        self.connection.commit()
        self.cursor.execute(sql3)
        self.connection.commit()
        self.cursor.execute(sql4)
        self.connection.commit()
        print("All tables dropped")


db = DatabaseConnection()
db.setuptables()
