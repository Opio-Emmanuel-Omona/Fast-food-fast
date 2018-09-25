'''using pytest to test the app'''
import json
import pytest
from app import app
import item
import order


#pylint: disable=missing-docstring
#pylint: disable=redefined-outer-name
orders_in = order.Order()

@pytest.fixture
def client():
    '''define a test client'''
    app.config['TESTING'] = True
    test_client = app.test_client()
    return test_client

class HelpAPI():
    #Helper methods for json tests
    def __init__(self):
        pass

    def post_json(self, client, url, json_dict):
        return client.post(url, data=json.dumps(json_dict), content_type='application/json')

    def put_json(self, client, url, json_dict):
        return client.put(url, data=json.dumps(json_dict), content_type='application/json')

    def delete_json(self, client, url):
        return client.delete(url)

    def json_of_response(self, response):
        return json.loads(response.data.decode('utf8'))

    #END helper methods

#API TESTS
class TestAPI():
    #Tests Begin
    def __init__(self):
        pass

    def test_dummy(self, client):
        response = client.get('/')
        assert b'Hello World!' in response.data

    def test_json(self, client):
        helper = HelpAPI()
        response = helper.post_json(client, '/add', {'key': 'value'})
        assert response.status_code == 200
        assert helper.json_of_response(response) == {'answer': 'value' * 2}

    def test_get_orders_api(self, client):
        response = client.get('/api/v1/orders')
        assert response.status_code == 200

    def test_place_order_api(self, client):
        helper = HelpAPI()
        response = helper.post_json(client, '/api/v1/orders',
                                    {'username': 'simon', 'item_name': 'chips', 'quantity': 1})
        assert response.status_code == 200
        orders_in.clear_orders()


    def test_one_order_api(self, client):
        helper = HelpAPI()
        response1 = helper.post_json(client, '/api/v1/orders',
                                     {'username': 'peter',
                                      'item_name': 'chips + chicken',
                                      'quantity': 1})
        response2 = client.get('/api/v1/orders/1')
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_update_order_api(self, client):
        helper = HelpAPI()
        response1 = helper.post_json(client, '/api/v1/orders',
                                     {'username': 'phiona', 'item_name': 'pork', 'quantity': 1})
        response2 = helper.put_json(client, '/api/v1/orders/1',
                                    {'username': 'phiona', 'item_name': 'pizza', 'quantity': 1})
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_delete_order_api(self, client):
        helper = HelpAPI()
        response1 = helper.post_json(client, '/api/v1/orders',
                                     {'username': 'wilful', 'item_name': 'matooke', 'quantity': 1})
        response2 = helper.delete_json(client, '/api/v1/orders/1')
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()

#ITEM TESTS
class TestItem():
    def __init__(self):
        pass

    def test_getItemQuantity(self):
        items = item.Item()
        assert items.get_item_quantity('Sandwich') == 0

    def test_setQuantity(self):
        items = item.Item()
        items.set_item_quantity('Pizza', 10)
        assert items.get_item_quantity('Pizza') == 10


#TEST ORDERS
class TestOrder():
    def __init__(self):
        pass

    def test_place_order(self):
        new_order = order.Order()
        new_order.place_new_order("Emma", "Pizza", 2)
        assert new_order.ORDERS == [
            {'order_id': 1, 'username': 'Emma', 'item_name': 'Pizza', 'quantity': 2}]
        orders_in.clear_orders()


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
