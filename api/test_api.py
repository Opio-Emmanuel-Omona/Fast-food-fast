'''using pytest to test the app'''
import json
import pytest
from app import app
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
    helper = HelpAPI()
    def test_dummy(self, client):
        response = client.get('/')
        assert b'Hello World!' in response.data

    def test_json(self, client):
        response = slef.helper.post_json(client, '/add', {'key': 'value'})
        assert response.status_code == 200
        assert self.helper.json_of_response(response) == {'answer': 'value' * 2}

    def test_get_orders_api(self, client):
        response = client.get('/api/v1/orders')
        assert response.status_code == 200

    def test_place_order_api(self, client):
        response = self.helper.post_json(client, '/api/v1/orders',
                                    {'username': 'simon', 'item_name': 'chips', 'quantity': 1})
        assert response.status_code == 200
        orders_in.clear_orders()


    def test_one_order_api(self, client):
        response1 = self.helper.post_json(client, '/api/v1/orders',
                                     {'username': 'peter',
                                      'item_name': 'chips + chicken',
                                      'quantity': 1})
        response2 = client.get('/api/v1/orders/1')
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_update_order_api(self, client):
        response1 = self.helper.post_json(client, '/api/v1/orders',
                                     {'username': 'phiona', 'item_name': 'pork', 'quantity': 1})
        response2 = self.helper.put_json(client, '/api/v1/orders/1',
                                    {'username': 'phiona', 'item_name': 'pizza', 'quantity': 1})
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()

    def test_delete_order_api(self, client):
        response1 = self.helper.post_json(client, '/api/v1/orders',
                                     {'username': 'wilful', 'item_name': 'matooke', 'quantity': 1})
        response2 = self.helper.delete_json(client, '/api/v1/orders/1')
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()


#TEST ORDERS
class TestOrder():
    def test_place_order(self):
        new_order = order.Order()
        new_order.place_new_order("Emma", "Pizza", 2)
        assert new_order.ORDERS == [
            {'order_id': 1, 'username': 'Emma', 'item_name': 'Pizza', 'quantity': 2}]
        orders_in.clear_orders()


#DATABASE TESTS
class TestDB():
    helper = HelpAPI()
    def test_register_new_user(self, client):
        response = self.helper.post_json(client, '/api/v1/auth/signup',
                                         {'username': 'phiona',
                                          'email': 'nanaphiona9@gmail.com',
                                          'phone_no': '+256758363563',
                                          'password': 'password'})
        assert response.status_code == 200

    def test_login_new_user(self, client):
        response = self.helper.post_json(client, '/api/v1/auth/login',
                              {'username': 'phiona',
                               'password': 'password'})
        assert response.status_code == 200

    def test_invalid_login(self, client):
        response = self.helper.post_json(client, '/api/v1/auth/login',
                              {'username': 'phiona',
                               'password': 'passwords'})
        assert response.status_code == 401



if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
