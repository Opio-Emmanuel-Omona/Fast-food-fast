'''The main application'''
from flask import Flask, jsonify, request, Response, json, redirect
from functools import wraps
from flasgger import Swagger, swag_from
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
                "type": "token",
                "name": "Authorization",
                "in": "header"
            }
        }
    })
orders = order.Order()

if not app.config['TESTING']:
    test_db = DatabaseConnection(False)

# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['ADMIN_KEY'] = 'thisistheadminkey'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http:127.0.0.1/5000/route?token=eyvjabd1e1bkjbcodklcnskdvbsn
        # token = request.args.get('token')

        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:], app.config['SECRET_KEY'])
            else:
                jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http:127.0.0.1/5000/route?token=eyvjabd1e1bkjbcodklcnskdvbsn
        # token = request.args.get('token')
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
    test_db.create_user(request.json)
    message = request.json['username'] + " account created successfully"
    return jsonify({'message': message}), 201


@app.route('/api/v2/auth/login', methods=['POST'])
@swag_from('../docs/signin.yml')
def signin():
    return test_db.signin(request.json), 200


@app.route('/api/v2/users/orders', methods=['POST'])
@swag_from('../docs/place_order.yml')
@token_required
def place_orders():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 403
    if token[0] == 'B':
        data = jwt.decode(token[7:], app.config['SECRET_KEY'])
    data = jwt.decode(token, app.config['SECRET_KEY'])
        
    user_dict = request.json
    user_dict['data'] = data
    test_db.add_order(user_dict)
    return jsonify({'message': 'Order has been placed'}), 201


@app.route('/api/v2/users/orders', methods=['GET'])
@swag_from('../docs/order_history.yml')
@token_required
def order_history():
    return test_db.order_history(), 200


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
