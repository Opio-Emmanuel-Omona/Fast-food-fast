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
test_db = DatabaseConnection(True)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:], app.config['SECRET_KEY'])
            else:
                jwt.decode(token, app.config['SECRET_KEY'])
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
                jwt.decode(token[7:], app.config['ADMIN_KEY'])
            else:
                jwt.decode(token, app.config['ADMIN_KEY'])
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
        return jsonify({'message': 'No data sent'}), 400
    if not data['username'] or not data['phone_no'] or not data['password'] or not data['email']:
        return jsonify({'message': 'Missing Fields'}), 400
    if (' ' in data['username'] or ' ' in data['email']):
        return jsonify({'message': 'Username or email cannot have spaces'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'message': 'Invalid Email'}), 400
    status = test_db.create_user(data)
    if status['status']:
        return jsonify(status), 201
    return jsonify(status), 409


@app.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../docs/signin.yml')
def signin():
    data = request.json
    if not data:
        return jsonify({'message': 'No data sent'}), 400
    if not data['username'] or not data['phone_no'] or not data['password'] or not data['email']:
        return jsonify({'message': 'Missing Fields'}), 400
    if (' ' in data['username'] or ' ' in data['email']):
        return jsonify({'message': 'Username or email cannot have spaces'}), 400
    return test_db.signin(data)


@app.route('/api/v2/users/orders', methods=['POST'])
@swag_from('../docs/place_order.yml')
@token_required
def place_orders():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    if token[0] == 'B':
        data = jwt.decode(token[7:], app.config['SECRET_KEY'])
    else:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        
    user_dict = request.json
    user_dict.update(data)
    test_db.add_order(user_dict)
    return jsonify({'message': 'Order has been placed'}), 201


@app.route('/api/v2/users/orders', methods=['GET'])
@swag_from('../docs/order_history.yml')
@token_required
def order_history():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    if token[0] == 'B':
        data = jwt.decode(token[7:], app.config['SECRET_KEY'])
    data = jwt.decode(token, app.config['SECRET_KEY'])
    history = test_db.order_history(data)

    return jsonify({'username': data['username'], 'history': history}), 200


@app.route('/api/v2/menu', methods=['POST'])
@swag_from('../docs/add_menu.yml')
@admin_required
def add_menu():
    test_db.add_menu(request.json)
    return jsonify({'message': 'Menu item successfully added'}), 201


@app.route('/api/v2/menu', methods=['GET'])
@swag_from('../docs/view_menu.yml')
@token_required
def menu():
    return test_db.menu(), 200


@app.route('/api/v2/orders', methods=['GET'])
@swag_from('../docs/orders.yml')
@admin_required
def fetch_all_orders():
    return test_db.fetch_all_orders(), 200


@app.route('/api/v2/orders/<string:order_id>', methods=['GET'])
@swag_from('../docs/specific_order.yml')
@admin_required
def fetch_specific_order(order_id):
    return test_db.fetch_specific_order(order_id), 200


@app.route('/api/v2/orders/<string:order_id>', methods=['PUT'])
@swag_from('../docs/update_order.yml')
@admin_required
def updated_order_status(order_id):
    user_dict = request.json
    user_dict['order_id'] = order_id
    test_db.update_order_status(user_dict)
    return jsonify({'message': 'Order status successfully altered'}), 200


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TESTING'] = False
