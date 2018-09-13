from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!" 


orders = [
    {
        'username' : 'opix',
        'item' : '1'
    },
    {
        'username' : 'phy',
        'item' : '2'
    }
]


@app.route('/v1/orders', methods=['GET'])
def all_orders():
    return jsonify({'orders' : orders})



if __name__ == "__main__":
    app.run(debug=True)