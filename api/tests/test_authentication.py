from help import HelpAPI
from api.views import app
from api.database import DatabaseConnection
import pytest

@pytest.fixture
def client():
    '''define a test client'''
    with app.app_context():
        app.config['TESTING'] = True
        test_client = app.test_client()   
    return test_client

def tearDown():
    DatabaseConnection().drop_tables
    

class TestAuthentication():
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
        assert response.status_code == 201

    def test_login_new_user(self, client):
        self.helper.post_json(
            client,
            '/api/v2/auth/signup',
            {
                'username': 'phiona',
                'email': 'nanaphiona9@gmail.com',
                'phone_no': '+256758363563',
                'password': 'password'
            })

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

    