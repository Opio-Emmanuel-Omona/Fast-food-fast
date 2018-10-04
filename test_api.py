# API TESTS
class TestAPI():
    # Tests Begin
    helper = HelpAPI()

    def test_get_orders_api(self, client):
        response = client.get('/api/v1/orders')
        assert response.status_code == 200

    def test_place_order_api(self, client):
        response = self.helper.post_json(
            client,
            '/api/v1/orders',
            {
                'username': 'simon',
                'item_name': 'chips',
                'quantity': 1
            })
        assert response.status_code == 201
        orders_in.clear_orders()

    def test_one_order_api(self, client):
        response1 = self.helper.post_json(
            client,
            '/api/v1/orders',
            {
                'username': 'peter',
                'item_name': 'chips + chicken',
                'quantity': 1
            })
        response2 = client.get('/api/v1/orders/1')
        assert response1.status_code == 201
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_update_order_api(self, client):
        response1 = self.helper.post_json(
            client,
            '/api/v1/orders',
            {
                'username': 'phiona',
                'item_name': 'pork',
                'quantity': 1
            })
        response2 = self.helper.put_json(
            client,
            '/api/v1/orders/1',
            {
                'username': 'phiona',
                'item_name': 'pizza',
                'quantity': 1
            })
        assert response1.status_code == 201
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_delete_order_api(self, client):
        response1 = self.helper.post_json(
            client,
            '/api/v1/orders',
            {
                'username': 'wilful',
                'item_name': 'matooke',
                'quantity': 1
            })
        response2 = self.helper.delete_json(
            client,
            '/api/v1/orders/1')
        assert response1.status_code == 201
        assert response2.status_code == 200
        orders_in.clear_orders()

