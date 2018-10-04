from api.order_old import Order_old

# TEST ORDERS
class TestOrder():
    order = Order_old()

    def test_place_order(self):
        self.order.place_new_order("Emma", "Pizza", 2)
        assert self.order.ORDERS == [
            {
                'order_id': 1,
                'username': 'Emma',
                'item_name': 'Pizza',
                'quantity': 2
            }]

    def test_delete_order(self):
        self.order.place_new_order("Opix", "Eggs", 1)
        self.order.delete_order(2)
        assert {'order_id':2, 'username':"Opix", 'item_name': "Eggs", 'quantity':1} not in self.order.ORDERS

    def test_update_order(self):
        self.order.place_new_order("Me", "Chips", 1)
        self.order.update_order(
            3,
            'Me',
            'Banana',
            1)
        assert {'order_id':3, 'username':"Me", 'item_name': "Chips", 'quantity':1} in self.order.ORDERS

    def test_get_one_order(self):
        assert 200 in self.order.get_order(1)

    def test_get_all_orders(self):
        assert self.order.get_all_orders() == self.order.ORDERS