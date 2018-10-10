from api.views import request
from api.database import DatabaseConnection


class Menu:
    def __init__(self):
        self.mydatabase = DatabaseConnection()
        self.mydatabase.create_menu_table()

    def add_menu(self):
        data = request.json
        if not data:
            return {'message': 'Empty Menu'}, 422
        if not data['item_name'] or not data['price']:
            return {'message': 'Missing Fields'}, 422
        status = self.mydatabase.add_menu(data)
        if status['status']:
            return status, 201
        return status, 409

    def get_menu(self):
        return self.mydatabase.menu(), 200
