'''The main application'''
from flask import Flask, jsonify, request, redirect
from functools import wraps
from flasgger import Swagger, swag_from
import re
import jwt
import order
from database import DatabaseConnection


app = Flask(__name__)  # pylint: disable=invalid-name
swagger = Swagger(
    app,
    template={
        "info": {
            "title": "Fast Food Fast API",
            "description": "A fast food delivery application"
        },
        "securityDefinitions": {
            "TokenHeader": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        }
    })
orders = order.Order()

# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


app.config['SECRET_KEY'] = 'qwertyuiopasdfghjkl'
app.config['ADMIN_KEY'] = 'lkjhgfdsapoiuytrewq'
# test_db = DatabaseConnection()

if __name__ != "__main__": 
    DatabaseConnection().setup()
else:
    DatabaseConnection().setuptables()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:].encode('utf-8'), app.config['SECRET_KEY'])
            else:
                jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid Token!'}), 403
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:].encode('utf-8'), app.config['ADMIN_KEY'])
            else:
                jwt.decode(token.encode('utf-8'), app.config['ADMIN_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def hello():
    return redirect('/apidocs')


@app.route('/api/v1/orders', methods=['GET'])
def all_orders():
    return jsonify({'orders': orders.ORDERS}), 200


@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def one_order(order_id):
    return jsonify({'orders': orders.get_order(order_id)}), 200
    

@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    orders.place_new_order(
        request.json['username'],
        request.json['item_name'],
        request.json['quantity'])
    return jsonify({'orders': orders.ORDERS}), 201


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    orders.update_order(
        order_id,
        request.json['username'],
        request.json['item_name'],
        request.json['quantity'])
    return jsonify({'orders': orders.ORDERS}), 200


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders.delete_order(order_id)
    return jsonify({'orders': orders.ORDERS}), 200


@app.route('/api/v2/auth/signup', methods=['POST'])
@swag_from('../docs/signup.yml')
def register():
    # connect add the data to the database
    data = request.json
    if not data:
        return jsonify({'message': 'No data sent'}), 422
    if not data['username'] or not data['phone_no'] or not data['password'] or not data['email']:
        return jsonify({'message': 'Missing Fields'}), 422
    if (' ' in data['username'] or ' ' in data['email']):
        return jsonify({'message': 'Username or email cannot have spaces'}), 422
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'message': 'Invalid Email'}), 422
    status = DatabaseConnection().create_user(data)
    if status['status']:
        return jsonify(status), 201
    return jsonify(status), 409


@app.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../docs/signin.yml')
def signin():
    data = request.json
    if not data:
        return jsonify({'message': 'No data sent'}), 422
    if not data['username'] or not data['password']:
        return jsonify({'message': 'Missing Fields'}), 422
    if (' ' in data['username']):
        return jsonify({'message': 'Username cannot have spaces'}), 422
    status = DatabaseConnection().signin(data)
    print(status)
    if status['status']:
        return jsonify(status)
    return jsonify(status), 401


@app.route('/api/v2/users/orders', methods=['POST'])
@swag_from('../docs/place_order.yml')
@token_required
def place_orders():
    # validate token
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    if token[0] == 'B':
        payload = jwt.decode(token[7:].encode('utf-8'), app.config['SECRET_KEY'])
    else:
        payload = jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'])
    
    # validate the input
    data = request.json
    if not data:
        return jsonify({'message': 'Empty Order'}), 422
    if not data['item_name'] or not data['quantity']:
        return jsonify({'message': 'Missing Fields'}), 422
    data.update(payload)
    status = DatabaseConnection().add_order(data)
    if status['status']:
        return jsonify(status), 201
    return jsonify(status), 409


@app.route('/api/v2/users/orders', methods=['GET'])
@swag_from('../docs/order_history.yml')
@token_required
def order_history():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    if token[0] == 'B':
        data = jwt.decode(token[7:].encode('utf-8'), app.config['SECRET_KEY'])
    data = jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'])
    history = DatabaseConnection().order_history(data)

    return jsonify({'username': data['username'], 'history': history}), 200


@app.route('/api/v2/menu', methods=['POST'])
@swag_from('../docs/add_menu.yml')
@admin_required
def add_menu():
    data = request.json
    if not data:
        return jsonify({'message': 'Empty Menu'}), 422
    if not data['item_name'] or not data['price']:
        return jsonify({'message': 'Missing Fields'}), 422
    status = DatabaseConnection().add_menu(data)
    if status['status']:
        return jsonify(status), 201
    return jsonify(status), 409


@app.route('/api/v2/menu', methods=['GET'])
@swag_from('../docs/view_menu.yml')
@token_required
def menu():
    return DatabaseConnection().menu(), 200


@app.route('/api/v2/orders', methods=['GET'])
@swag_from('../docs/orders.yml')
@admin_required
def fetch_all_orders():
    return DatabaseConnection().fetch_all_orders(), 200


@app.route('/api/v2/orders/<string:order_id>', methods=['GET'])
@swag_from('../docs/specific_order.yml')
@admin_required
def fetch_specific_order(order_id):
    return DatabaseConnection().fetch_specific_order(order_id), 200


@app.route('/api/v2/orders/<string:order_id>', methods=['PUT'])
@swag_from('../docs/update_order.yml')
@admin_required
def updated_order_status(order_id):
    user_dict = request.json
    if not user_dict:
        return jsonify({'message': 'No data sent'}), 422
    if not user_dict['status_name']:
        return jsonify({'message': 'Missing Fields'}), 422
    user_dict['order_id'] = order_id
    status = DatabaseConnection().update_order_status(user_dict)
    if status['status']:
        return jsonify(status), 200
    elif ('wrong status' in status['message']):
        return jsonify(status), 409
    else:
        return jsonify(status), 400


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TESTING'] = False
