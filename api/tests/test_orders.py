from help import HelpAPI
from api.views import app
import pytest

@pytest.fixture
def client():
    '''define a test client'''
    with app.app_context():
        app.config['TESTING'] = True
        test_client = app.test_client()   
    return test_client

class TestOrders:
    helper = HelpAPI

    def test_place_order(self, client):
        # Login as admin and add item to menu
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
                'item_name': 'Fried Eggs',
                'price': '3000'
            },
            response1.json['token']
        )
        # Ensure that you are logged in as user
        response3 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })
        response4 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response3.json['username'],
                'item_name': 'Fried Eggs',
                'quantity': '1',
            },
            response3.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201
        assert response3.status_code == 200
        assert response4.status_code == 201

    def test_order_history(self, client):
        response1 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response2 = client.get(
            '/api/v2/users/orders',
            headers={'Authorization': response1.json['token']}
        )
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_update_order_status(self, client):
        # admin adds an order to menu
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
                'item_name': 'Chicken',
                'price': '5000'
            },
            response1.json['token']
        )
        # user places an order
        response3 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'phiona',
                'password': 'password'
            })

        response4 = self.helper.post_json_with_token(
            client,
            '/api/v2/users/orders',
            {
                'username': response3.json['username'],
                'item_name': 'Chicken',
                'quantity': '1'
            },
            response3.json['token']
        )
    
        # admin then updates it
        response5 = self.helper.post_json(
            client,
            '/api/v2/auth/login',
            {
                'username': 'admin',
                'password': 'password'
            }
        )
        response6 = self.helper.put_json_with_token(
            client,
            '/api/v2/orders/0',
            {
                'username': response3.json['username'],
                'item_name': 'Fried Eggs',
                'status_name': 'Processing',
            },
            response5.json['token']
        )
        assert response1.status_code == 200
        assert response2.status_code == 201
        assert response3.status_code == 200
        assert response4.status_code == 201
        assert response5.status_code == 200
        assert response6.status_code == 200
