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


class TestMenu:
    helper = HelpAPI()

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
                    'item_name': 'Chips + Chicken',
                    'price': '5000',
                },
                response1.json['token']
            )
            
            assert response1.status_code == 200
            assert response2.status_code == 201

        # def test_view_menu(self):
        #     pass