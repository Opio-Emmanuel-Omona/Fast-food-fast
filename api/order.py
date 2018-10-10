from api.database import DatabaseConnection
from api.views import request
import jwt


class Order():
    def __init__(self):
        self.mydatabase = DatabaseConnection()
        self.mydatabase.create_order_table()

    def place_orders(self):
        # validate token
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 403
        if token[0] == 'B':
            payload = jwt.decode(token[7:].encode('utf-8'), 'qwertyuiopasdfghjkl')
        else:
            payload = jwt.decode(token.encode('utf-8'), 'qwertyuiopasdfghjkl')
        
        # validate the input
        data = request.json
        if not data:
            return {'message': 'Empty Order'}, 422
        if not data['item_name'] or not data['quantity']:
            return {'message': 'Missing Fields'}, 422
        data.update(payload)
        status = self.mydatabase.add_order(data)
        if status['status']:
            return status, 201
        return status, 409

    def order_history(self):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 403
        if token[0] == 'B':
            data = jwt.decode(token[7:].encode('utf-8'), 'qwertyuiopasdfghjkl')
        data = jwt.decode(token.encode('utf-8'), 'qwertyuiopasdfghjkl')
        history = self.mydatabase.order_history(data)

        return {'username': data['username'], 'history': history}, 200

    def fetch_all_orders(self):
        return self.mydatabase.fetch_all_orders(), 200

    def fetch_specific_order(self, order_id):
        return self.mydatabase.fetch_specific_order(order_id), 200

    def updated_order_status(self, order_id):
        user_dict = request.json
        if not user_dict:
            return {'message': 'No data sent'}, 422
        if not user_dict['status_name']:
            return {'message': 'Missing Fields'}, 422
        user_dict['order_id'] = order_id
        status = self.mydatabase.update_order_status(user_dict)
        if status['status']:
            return status, 200
        elif ('wrong status' in status['message']):
            return status, 409
        else:
            return status, 400
