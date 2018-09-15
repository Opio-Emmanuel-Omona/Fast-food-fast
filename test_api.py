import pytest
import requests
import json
from app import app


@pytest.fixture
def client(request):
    app.config['TESTING'] = True
    test_client = app.test_client()

    def teardown():
        pass
    
    request.addfinalizer(teardown)
    return test_client

def post_json(client, url, json_dict):
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def put_json(client, url, json_dict):
    return client.put(url, data=json.dumps(json_dict), content_type='application/json')

def delete_json(client, url):
    return client.delete(url)

def json_of_response(response):
    return json.loads(response.data.decode('utf8'))

def test_dummy(client):
    response = client.get('/')
    assert b'Hello World!' in response.data

def test_json(client):
    response = post_json(client, '/add', {'key': 'value'})
    assert response.status_code == 200
    assert json_of_response(response) == {'answer': 'value' * 2}

def test_getOrders(client):
    response = client.get('/api/v1/orders')
    assert response.status_code == 200

def test_placeOrder(client):
    response = post_json(client, '/api/v1/orders', {'id': '1', 'username': 'simon', 'item': 'chips'})
    assert response.status_code == 200

def test_oneOrder(client):
    response1 = post_json(client, '/api/v1/orders', {'id': '2', 'username': 'peter', 'item': 'chips + chicken'})
    response2 = client.get('/api/v1/orders/1')
    assert response1.status_code == 200
    assert response2.status_code == 200

def test_updateOrder(client):
    response1 = post_json(client, '/api/v1/orders', {'id': '3', 'username': 'phiona', 'item': 'pork'})
    response2 = put_json(client, '/api/v1/orders/3', {'username': 'phiona', 'item': 'pizza'})
    assert response1.status_code == 200
    assert response2.status_code == 200

def test_deleteOrder(client):
    response1 = post_json(client, '/api/v1/orders', {'id': '4', 'username': 'wilful', 'item': 'matooke'}) 
    response2 = delete_json(client, '/api/v1/orders/4')
    assert response1.status_code == 200
    assert response2.status_code == 200


if __name__=="__main__":
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
