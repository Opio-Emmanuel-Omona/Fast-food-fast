# TEST ORDERS
class TestOrder():
    def test_place_order(self):
        new_order = order.Order()
        new_order.place_new_order("Emma", "Pizza", 2)
        assert new_order.ORDERS == [
            {
                'order_id': 1,
                'username': 'Emma',
                'item_name': 'Pizza',
                'quantity': 2
            }]
        orders_in.clear_orders()
