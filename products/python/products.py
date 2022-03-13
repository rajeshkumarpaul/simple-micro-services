from flask import Flask, request, jsonify
from from_root import from_root
from json import load

app = Flask(__name__)

with from_root('database', "products.json").open('rb') as f:
    products_list = load(f)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Unable to find werkzeug.server.shutdown')
    func()

@app.route('/', methods=['GET'])
def hello():
    return 'Products service - OK', 200

@app.route('/products', methods=['GET'])
def products():
    return jsonify(products_list), 200

@app.route('/products/<id>', methods=['GET'])
def product_by_id(id):
    for product in products_list:
        if product['id'] == id:
            print("Returning product - ", product['id'])
            return product
    return {}, 400

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8083, debug=True)
