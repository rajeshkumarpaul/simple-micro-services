from flask import Flask, request, jsonify
from from_root import from_root
from json import load
import requests

app = Flask(__name__)

with from_root('database', "users.json").open('rb') as f:
    users_list = load(f)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Unable to find werkzeug.server.shutdown')
    func()

@app.route('/', methods=['GET'])
def hello():
    return 'Users service - OK', 200

@app.route('/users', methods=['GET'])
def users():
    return jsonify(users_list), 200

@app.route('/users/<name>', methods=['GET'])
def user_by_id(name):
    result = [{ "name": name,'orders': [] }]
    for  user in users_list:
        if user['name'] == name:
            for order in user["orders"]:
                res = requests.get("http://192.168.0.242:8082/orders/{}".format(order['id']))
                result[0]['orders'].append(res.json())
    return jsonify(result), 200

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8081, debug=True)
