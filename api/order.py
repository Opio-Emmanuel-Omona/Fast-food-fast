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
