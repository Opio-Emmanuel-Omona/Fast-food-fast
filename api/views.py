'''The main application'''
from flask import Flask, jsonify, request, redirect, render_template, url_for
from functools import wraps
from flasgger import Swagger, swag_from
from flask_restful import Resource, Api, reqparse
from api.order import Order
from api.user import User
from api.menu import Menu

import jwt
from api.database import DatabaseConnection


app = Flask(__name__)  # pylint: disable=invalid-name
Swagger(
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

api = Api(app)

# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


app.config['SECRET_KEY'] = 'qwertyuiopasdfghjkl'
app.config['ADMIN_KEY'] = 'lkjhgfdsapoiuytrewq'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Missing token!'}, 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:].encode('utf-8'), app.config['SECRET_KEY'])
            else:
                jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'])
        except:
            return {'message': 'Invalid Token!'}, 403
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 403
        try:
            if token[0] == 'B':
                jwt.decode(token[7:].encode('utf-8'), app.config['ADMIN_KEY'])
            else:
                jwt.decode(token.encode('utf-8'), app.config['ADMIN_KEY'])
        except:
            return {'message': 'Token is invalid!'}, 403
        
        return f(*args, **kwargs)
    return decorated

def validate_token():
    # validate token
    token = request.headers.get('Authorization')
    if not token:
        return {'message': 'Token is missing!'}, 403
    if token[0] == 'B':
        payload = jwt.decode(token[7:].encode('utf-8'), app.config['SECRET_KEY'])
    else:
        payload = jwt.decode(token.encode('utf-8'), app.config['SECRET_KEY'])
    return payload

class Orders(Resource):
    @admin_required
    @swag_from('../docs/orders.yml')
    def get(self):
        return Order().fetch_all_orders() 


class OrderX(Resource):
    @admin_required
    @swag_from('../docs/specific_order.yml')
    def get(self, order_id):
        return Order().fetch_specific_order(order_id)

    @admin_required
    @swag_from('../docs/update_order.yml')
    def put(self, order_id):
        return Order().updated_order_status(order_id)


class Menus(Resource):
    @token_required
    @swag_from('../docs/view_menu.yml')
    def get(self):
        return Menu().get_menu()

    @admin_required
    @swag_from('../docs/add_menu.yml')
    def post(self):
        return Menu().add_menu()


class UserOrder(Resource):
    @token_required
    @swag_from('../docs/order_history.yml')
    def get(self):
        return Order().order_history()

    @token_required
    @swag_from('../docs/place_order.yml')
    def post(self):
        return Order().place_orders()


class Login(Resource):
    @swag_from('../docs/signin.yml')
    def post(self):
        return User().signin()


class Signup(Resource):
    @swag_from('../docs/signup.yml')
    def post(self):
        return User().register()


api.add_resource(Signup, '/api/v2/auth/signup')
api.add_resource(Login, '/api/v2/auth/login')
api.add_resource(Menus, '/api/v2/menu')
api.add_resource(UserOrder, '/api/v2/users/orders')
api.add_resource(OrderX, '/api/v2/orders/<string:order_id>')
api.add_resource(Orders, '/api/v2/orders/')


@app.route("/")
def hello():
    return redirect('/apidocs')

@app.route('/signup')
def signupUI():
    return render_template('signup.html')

@app.route('/login')
def loginUI():
    return render_template('signin.html')

@app.route('/home')
# @token_required
def homeUI():
    return render_template('home.html')
