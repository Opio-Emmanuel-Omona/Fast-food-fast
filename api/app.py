'''The main application'''
from flask import Flask, jsonify, request, Response, json, make_response
from functools import wraps
import psycopg2
import jwt
import datetime
import order
app = Flask(__name__)  # pylint: disable=invalid-name
orders = order.Order()


# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config['ADMIN_KEY'] = 'thisistheadminkey'

class JsonResponse(Response):  # pylint: disable=too-many-ancestors
    def __init__(self, json_dict, status=200):
        super(JsonResponse, self).__init__(response=json.dumps(json_dict),
                                           status=status, mimetype='application/json')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http:127.0.0.1/5000/route?token=eyvjabd1e1bkjbcodklcnskdvbsn
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)

    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #http:127.0.0.1/5000/route?token=eyvjabd1e1bkjbcodklcnskdvbsn
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['ADMIN_KEY'])
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
        request.json['username'], request.json['item_name'], request.json['quantity'])
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    orders.update_order(
        order_id, request.json['username'], request.json['item_name'], request.json['quantity'])
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders.delete_order(order_id)
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v2/auth/signup', methods=['POST'])
def register():
    #connect add the data to the database
    connection = psycopg2.connect(database="fast_food_fast_db", user="postgres", password="P@ss1234", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    sql = "INSERT INTO \"user\" (username, email, phone_no, password) VALUES('"+request.json['username']+"','"+request.json['email']+"','"+request.json['phone_no']+"','"+request.json['password']+"');"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return request.json['username'] + "Account created successfully"


@app.route('/api/v2/auth/login', methods=['POST'])
def signin():
    #check if the creditentials posted are in the database
    connection = psycopg2.connect(database="fast_food_fast_db", user="postgres", password="P@ss1234", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    sql = "SELECT username, password FROM \"user\";"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        if row[0] == request.json['username'] and row[1] == request.json['password']:
            #then login
            #give token based authentication to this user
            token = jwt.encode({'user': request.json['username'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                                app.config['SECRET_KEY'])
            connection.commit()
            connection.close()
            return jsonify({'user': request.json['username'], 'token': token})

    #ADMIN login
    if request.json['username'] == 'admin' and request.json['password'] == 'password':
        token = jwt.encode({'user': request.json['username'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                            app.config['ADMIN_KEY'])
        connection.commit()
        connection.close()
        return jsonify({'user': request.json['username'], 'token': token})

    connection.commit()
    connection.close()
    resp = JsonResponse(json_dict={'answer': 401}, status=401)
    return resp #login failed


@app.route('/api/v2/users/orders', methods=['POST'])
@token_required
def place_orders():
    connection = psycopg2.connect(database="fast_food_fast_db", user="postgres", password="P@ss1234", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    sql = "INSERT INTO \"order\" (username, item_name, quantity) VALUES('"+request.json['username']+"','"+request.json['item_name']+"','"+request.json['quantity']+"');"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return "Order has been placed" #the order placed


@app.route('/api/v2/menu', methods=['POST'])
@admin_required
def add_menu():
    connection = psycopg2.connect(database="fast_food_fast_db", user="postgres", password="P@ss1234", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    sql = "INSERT INTO \"menu\" (item_name) VALUES('"+request.json['item_name']+"');"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return "Menu item successfully added" 


@app.route('/api/v2/menu', methods=['GET'])
@token_required
def menu():
    connection = psycopg2.connect(database="fast_food_fast_db", user="postgres", password="P@ss1234", host="127.0.0.1", port="5432")
    cursor = connection.cursor()
    sql = "SELECT * FROM \"menu\";"
    cursor.execute(sql)
    rows = cursor.fetchall()
    menu = []
    for row in rows:
        menu.append(row[1])
    connection.commit()
    connection.close()
    return jsonify({'menu': menu})


if __name__ == "__main__":
    app.run(debug=True)
