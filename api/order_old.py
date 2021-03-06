from tests.help import json

class Order_old:
    '''Handles all orders'''
    ORDERS = []

    def __init__(self):
        self.ORDERS = []
        self.order_id = 1
        self.username = ''
        self.item_name = ''
        self.quantity = 0

    def place_new_order(self, username, item_name, quantity):
        '''First check whether the username and item_name exist then update the quantity'''
        order = [
            ordering for ordering in self.ORDERS if ordering['username'] == username
            and ordering['item_name'] == item_name]
        if not order:
            order_dict = {
                "order_id": self.order_id,
                "username": username,
                "item_name": item_name,
                "quantity": quantity
            }
            self.ORDERS.append(order_dict)
        else:
            order[0]['quantity'] += quantity

        self.order_id += 1

    def update_order(self, order_id, username, item_name, quantity):
        '''change the username item_name and quantity but not the id'''
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        order[0]['username'] = username
        order[0]['item_name'] = item_name
        order[0]['quantity'] = quantity

    def delete_order(self, order_id):
        '''deletes by id'''
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        self.ORDERS.remove(order[0])

    def get_order(self, order_id):
        '''returns a specific order'''
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        return order, 200

    def clear_orders(self):
        '''resets the orders to empty'''
        self.ORDERS = []

    def get_all_orders(self):
        return self.ORDERS
