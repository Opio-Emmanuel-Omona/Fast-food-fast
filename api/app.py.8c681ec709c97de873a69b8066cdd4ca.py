from flask import Flask, jsonify, request, Response, json
app = Flask(__name__)


orders = []

class JsonResponse(Response):
    def __init__(self, json_dict, status=200):
        super(JsonResponse, self).__init__(response=json.dumps(json_dict), status=status, mimetype='application/json')


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
    return jsonify({'orders': orders})


@app.route('/api/v1/orders/<string:id>', methods=['GET'])
def one_order(id):
    order = [ordering for ordering in orders if ordering['id'] == id]
    return jsonify({'orders': order[0]})


@app.route('/api/v1/orders', methods=['POST'])
def place_order():
    order = {'id': request.json['id'], 'username': request.json['username'], 'item': request.json['item']}
    orders.append(order)
    return jsonify({'orders': orders})


@app.route('/api/v1/orders/<string:id>', methods=['PUT'])
def update_order(id):
    order = [ordering for ordering in orders if ordering['id'] == id]
    order[0]['username'] = request.json['username']
    order[0]['item'] = request.json['item']
    return jsonify({'orders': order[0]})


@app.route('/api/v1/orders/<string:id>', methods=['DELETE'])
def delete_order(id):
    order = [ordering for ordering in orders if ordering['id'] == id]
    orders.remove(order[0])
    return jsonify({'orders': orders})


if __name__ == "__main__":
    app.run(debug=True)
