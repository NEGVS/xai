# app.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# java 可以调用python程序

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    print(data)
    print(type(data))
    print("-------")
    # print(str(data))
    # json_data = json.loads(str(data))
    # print(json_data)
    for i, j in data:
        print(i)
        print(j)
    print("-------")
    a = data['a']
    b = data['b']
    result = a + b
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
