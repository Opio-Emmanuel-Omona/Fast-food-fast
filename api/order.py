import item


class Order():
    ORDERS = []

    def __init__(self):
        self.ORDERS = []
        self.order_id = 1
        self.username = ''
        self.item_name = ''
        self.quantity = 0

    def place_new_order(self, username, item_name, quantity):
        order_dict = {
            "order_id": self.order_id,
            "username": username,
            "item_name": item_name,
            "quantity": quantity
        }
        self.ORDERS.append(order_dict)
        self.order_id += 1

    def update_order(self, order_id, username, item_name, quantity):
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        order[0]['username'] = username
        order[0]['item_name'] = item_name
        order[0]['quantity'] = quantity

    def delete_order(self, order_id):
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        self.ORDERS.remove(order[0])

    def get_order(self, order_id):
        order = [
            ordering for ordering in self.ORDERS if ordering['order_id'] == order_id]
        return order

    def clear_orders(self):
        self.ORDERS = []
