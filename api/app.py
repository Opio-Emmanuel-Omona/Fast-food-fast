'''The main application'''
from flask import Flask, jsonify, request
import order
app = Flask(__name__)  # pylint: disable=invalid-name
orders = order.Order()

# pylint: disable=missing-docstring
# pylint: disable=redefined-outer-name


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
    if not request.json:
        return "Empty Order"
    if request.json['username'] == '' or request.json['item_name'] == '' or request.json['quantity'] == '':
        return "Incomplete Order"
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


if __name__ == "__main__":
    app.run(debug=True)
