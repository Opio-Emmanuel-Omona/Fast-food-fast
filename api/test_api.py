'''using pytest to test the app'''
import json
import pytest
from app import app
import order
import database


# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name
orders_in = order.Order()
test_db = database.DatabaseConnection()


@pytest.fixture
def client():
    '''define a test client'''
    with app.app_context():
        app.config['TESTING'] = True
        test_client = app.test_client()   
    return test_client


class HelpAPI():
    # Helper methods for json tests
    def post_json(self, client, url, json_dict):
        return client.post(
            url,
            data=json.dumps(json_dict),
            content_type='application/json')

    def post_json_with_token(self, client, url, json_dict, token):
        return client.post(
            url,
            data=json.dumps(json_dict),
            headers=dict(
                Authorization='Bearer ' + token
            ),
            content_type='application/json'
        )

    def put_json_with_token(self, client, url, json_dict, token):
        return client.put(
            url,
            data=json.dumps(json_dict),
            headers=dict(
                Authorization='Bearer ' + token
            ),
            content_type='application/json'
        )

    def put_json(self, client, url, json_dict):
        return client.put(
            url,
            data=json.dumps(json_dict),
            content_type='application/json')

    def delete_json(self, client, url):
        return client.delete(url)

    def json_of_response(self, response):
        return json.loads(response.data.decode('utf8'))

    # END helper methods


# API TESTS
class TestAPI():
    # Tests Begin
    helper = HelpAPI()

    def test_dummy(self, client):
        response = client.get('/')
        assert b'Hello World!' in response.data

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
        assert response.status_code == 200
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
        assert response1.status_code == 200
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
        assert response1.status_code == 200
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
        assert response1.status_code == 200
        assert response2.status_code == 200
        orders_in.clear_orders()


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


# DATABASE TESTS
class TestDB():
    helper = HelpAPI()

    def test_register_new_user(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/signup',
            {
                'username': 'phiona',
                'email': 'nanaphiona9@gmail.com',
                'phone_no': '+256758363563',
                'password': 'password'
            })
        assert response.status_code == 200

    def test_login_new_user(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })
        assert response.json['username'] == 'phiona'
        assert response.status_code == 200
        # delete the user afterwards

    def test_invalid_login(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'passwords'
            })
        assert response.status_code == 401

    def test_admin_login(self, client):
        response = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        assert response.status_code == 200

    def test_add_menu_item(self, client):
        # Login as admin
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/menu',
            {
                'item_name': 'admin_item',
                'price': '5000',
            },
            response1.json['token']
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_place_order(self, client):
        # Ensure that you are logged in as user
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response1.json['username'],
                'item_name': 'Fried Eggs',
                'quantity': '1',
            },
            response1.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201

    # def test_order_history(self, client):
    #     response1 = self.helper.post_json(
    #         client,
    #         '/api/v2/auth/login',
    #         {
    #             'username': 'phiona',
    #             'password': 'password'
    #         })

    #     response2 = client.get(
    #         '/api/v2/users/orders',
    #         headers=dict(
    #             Authorization='Bearer ' + response1.json['token']
    #         )
    #     )
    #     assert response1.status_code == 200
    #     assert response2.status_code == 200

    # def test_fetch_specific_order(self):
    #     # login as admin
    #     response1 = self.helper.post_json(
    #         client,
    #         '/api/v2/auth/login',
    #         {
    #             'username': 'phiona',
    #             'password': 'password'
    #         })

    #     response2 = client.get(
    #         '/api/v2/orders/0',
    #         headers=dict(
    #             Authorization='Bearer ' + response1.json['token']
    #         )
    #     )
    #     assert response1.status_code == 200
    #     assert response2.status_code == 200

    # def test_fetch_all_orders(self):
    #     pass

    # def test_view_menu(self):
    #     pass

    def test_update_order_status(self, client):
        # user first places an order
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response2 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response1.json['username'],
                'item_name': 'Fried Eggs',
                'quantity': '1'
            },
            response1.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201

        # admin then updates it
        response3 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response4 = self.helper.put_json_with_token(
            client,
            '/api/v2/orders/0',
            {
                'username': response1.json['username'],
                'item_name': 'Fried Eggs',
                'status_name': 'Processing',
            },
            response3.json['token']
        )
        assert response3.status_code == 200
        assert response4.status_code == 200


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
