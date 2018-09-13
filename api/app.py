from flask import Flask, jsonify
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


orders = [
    {
        'id': '1',
        'username': 'opix',
        'item': '1'
    },
    {
        'id': '2',
        'username': 'phy',
        'item': '2'
    }
]


@app.route('/api/v1/orders', methods=['GET'])
def all_orders():
    return jsonify({'orders': orders})


@app.route('/api/v1/orders/<string:id>', methods=['GET'])
def one_order(id):
    order = [ordering for ordering in orders if ordering['id'] == id]
    return jsonify({'orders': order[0]})


if __name__ == "__main__":
    app.run(debug=True)
