'''The main application'''
from flask import Flask, jsonify, request, Response, json
import order
app = Flask(__name__) #pylint: disable=invalid-name
orders = order.Order()


#pylint: disable=missing-docstring
#pylint: disable=redefined-outer-name

class JsonResponse(Response): #pylint: disable=too-many-ancestors
    def __init__(self, json_dict, status=200):
        super(JsonResponse, self).__init__(response=json.dumps(json_dict),
                                           status=status, mimetype='application/json')


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/add', methods=['POST'])
def add():
    json = request.get_json()
    resp = JsonResponse(json_dict={'answer': json['key'] * 2}, status=200)
    return resp


@app.route('/api/v1/orders', methods=['GET'])
def all_orders():
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<string:order_id>', methods=['GET'])
def one_order(order_id):
    order = [ordering for ordering in orders.ORDERS if ordering['id'] == order_id]
    return jsonify({'orders': order[0]})


@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    orders.place_new_order(request.json['username'], request.json['item'], request.json['quantity'])
    return jsonify({'orders': orders.ORDERS})


@app.route('/api/v1/orders/<string:order_id>', methods=['PUT'])
def update_order(order_id):
    order = [ordering for ordering in orders.ORDERS if ordering['id'] == order_id]
    order[0]['username'] = request.json['username']
    order[0]['item'] = request.json['item']
    return jsonify({'orders': order[0]})


@app.route('/api/v1/orders/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = [ordering for ordering in orders.ORDERS if ordering['id'] == order_id]
    orders.ORDERS.remove(order[0])
    return jsonify({'orders': orders.ORDERS})


if __name__ == "__main__":
    app.run(debug=True)
