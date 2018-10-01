'''The main application'''
from flask import Flask, jsonify, request, Response, json
from functools import wraps
import jwt
import order
from database import DatabaseConnection


app = Flask(__name__)  # pylint: disable=invalid-name
orders = order.Order()
test_db = DatabaseConnection()

# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['ADMIN_KEY'] = 'thisistheadminkey'


class JsonResponse(Response):  # pylint: disable=too-many-ancestors
    def __init__(self, json_dict, status=200):
        super(JsonResponse, self).__init__(
            response=json.dumps(json_dict),
            status=status,
            mimetype='application/json')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # http:127.0.0.1/5000/route?token=eyvjabd1e1bkjbcodklcnskdvbsn
        # token = request.args.get('token')

        if not app.config['TESTING']:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
                jwt.decode(token[7:], app.config['SECRET_KEY'])
            except:
                return jsonify({'message': 'Token is invalid!'}), 403
        else:
            token = request.json['token']
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
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
        if not app.config['TESTING']:
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
                jwt.decode(token[7:], app.config['ADMIN_KEY'])
            except:
                return jsonify({'message': 'Token is invalid!'}), 403
        else:
            token = request.json['token']
            if not token:
                return jsonify({'message': 'Token is missing!'}), 403
            try:
                jwt.decode(token, app.config['ADMIN_KEY'])
            except:
                return jsonify({'message': 'Token is invalid!'}), 403
        
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/api/v1/orders', methods=['GET'])
def all_orders():
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def one_order(order_id):
    return jsonify({'orders': orders.get_order(order_id)})


@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    orders.place_new_order(
        request.json['username'],
        request.json['item_name'],
        request.json['quantity'])
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    orders.update_order(
        order_id,
        request.json['username'],
        request.json['item_name'],
        request.json['quantity'])
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders.delete_order(order_id)
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v2/auth/signup', methods=['POST'])
def register():
    # connect add the data to the database
    test_db.create_user(request.json)
    return request.json['username'] + " account created successfully"


@app.route('/api/v2/auth/login', methods=['POST'])
def signin():
    return test_db.signin(request.json)


@app.route('/api/v2/users/orders', methods=['POST'])
@token_required
def place_orders():
    if not app.config['TESTING']:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
            
        data = jwt.decode(token[7:], app.config['SECRET_KEY'])
            
    else:
        token = request.json['token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        data = jwt.decode(token, app.config['SECRET_KEY'])
        
    user_dict = request.json
    user_dict['data'] = data
    test_db.add_order(user_dict)
    return "Order has been placed", 201


@app.route('/api/v2/users/orders', methods=['GET'])
@token_required
def order_history():
    return test_db.order_history()


@app.route('/api/v2/menu', methods=['POST'])
@admin_required
def add_menu():
    test_db.add_menu(request.json)
    return "Menu item successfully added"


@app.route('/api/v2/menu', methods=['GET'])
@token_required
def menu():
    return test_db.menu()


@app.route('/api/v2/orders', methods=['GET'])
@admin_required
def fetch_all_orders():
    return test_db.fetch_all_orders()


@app.route('/api/v2/orders/<string:order_id>', methods=['GET'])
@admin_required
def fetch_specific_order(order_id):
    return test_db.fetch_specific_order(order_id)


@app.route('/api/v2/orders/<string:order_id>', methods=['PUT'])
@admin_required
def updated_order_status(order_id):
    user_dict = request.json
    user_dict['order_id'] = order_id
    test_db.update_order_status(user_dict)
    return "Order status successfully altered"


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TESTING'] = False
