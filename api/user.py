from api.views import request
import re
from api.database import DatabaseConnection


class User:
    def __init__(self):
        self.mydatabase = DatabaseConnection()
        self.mydatabase.create_order_table()

    def signin(self):
        data = request.json
        if not data:
            return {'message': 'No data sent'}, 422
        if not data['username'] or not data['password']:
            return {'message': 'Missing Fields'}, 422
        if (' ' in data['username']):
            return {'message': 'Username cannot have spaces'}, 422
        status = self.mydatabase.signin(data)
        print(status)
        if status['status']:
            return status
        return status, 401

    def register(self):
        # connect add the data to the database
        data = request.json
        if not data:
            return {'message': 'No data sent'}, 422
        if not data['username'] or not data['phone_no'] or not data['password'] or not data['email']:
            return {'message': 'Missing Fields'}, 422
        if (' ' in data['username'] or ' ' in data['email']):
            return {'message': 'Username or email cannot have spaces'}, 422
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return {'message': 'Invalid Email'}, 422
        status = self.mydatabase.create_user(data)
        print(status)
        if status['status']:
            return status, 201
        return status, 409