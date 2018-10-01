import psycopg2


class DatabaseConnection():
    def __init__(self):
        self.connection = psycopg2.connect(
            database="fast_food_fast_db",
            user="postgres",
            password="P@ss1234",
            host="127.0.0.1",
            port="5432"
        )
        self.cursor = self.connection.cursor()
        self.create_user_table()

    def create_user_table(self):
        sql = (
            '''CREATE TABLE IF NOT EXISTS "test" (
                username character varying(20) PRIMARY KEY,
                email character varying(50) NOT NULL,
                phone_no character varying(15) NOT NULL,
                password character varying(20) NOT NULL
            );'''
        )
        self.cursor.execute(sql)
        print ("Table created successfully")
        self.connection.commit()
        
    def create_user(self, user_dict):
        ''' add user to table '''
        sql = "INSERT INTO \"user\"(username, email, phone_no, password) VALUES('"+user_dict['username']+"','"+user_dict['email']+"','"+user_dict['phone_no']+"','"+user_dict['password']+"');"
        self.cursor.execute(sql)
        print ("Table created successfully")
        self.connection.commit()
        
    def close_connection(self):
        self.connection.close()
