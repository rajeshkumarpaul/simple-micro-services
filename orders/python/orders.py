from flask import Flask, request, jsonify
from from_root import from_root
from json import load
import requests

app = Flask(__name__)

with from_root('database', "orders.json").open('rb') as f:
    orders_list = load(f)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Unable to find werkzeug.server.shutdown')
    func()

@app.route('/', methods=['GET'])
def hello():
    return 'Orders service - OK', 200

@app.route('/orders', methods=['GET'])
def orders():
    return jsonify(orders_list), 200

@app.route('/orders/<id>', methods=['GET'])
def order_by_id(id):
    result = [{ "id": id,'products': [] }]
    for order in orders_list:
        if order['id'] == id:
            for product in order["products"]:
                res = requests.get("http://192.168.0.242:8083/products/{}".format(product['id']))
                result[0]['products'].append(res.json())
    return jsonify(result), 200

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8082, debug=True)
