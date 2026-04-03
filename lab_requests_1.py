import random
import time
from threading import Thread
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

operations = ['sum', 'sub', 'mul', 'div']


# Реализация запросов
@app.route('/number/', methods=['GET', 'POST', 'DELETE'])
def handle_number():
    if request.method == 'GET':
        value = int(request.args.get('param', 1))
        result_number = random.randint(1, 10) * value

    elif request.method == 'POST':
        value = int(request.json.get('jsonParam', 1))
        result_number = random.randint(1, 10) * value

    else:  # DELETE
        result_number = random.randint(1, 10)

    return jsonify({
        'number': result_number,
        'operation': random.choice(operations)
    })


# функция вычисления    
def execute_op(x, y, op_type):
    if op_type == 'sum':
        return x + y
    elif op_type == 'sub':
        return x - y
    elif op_type == 'mul':
        return x * y
    elif op_type == 'div':
        return x / y if y != 0 else 0


# выполнение операций
def run_client():
    endpoint = 'http://127.0.0.1:5000/number/'

    # GET
    response_get = requests.get(endpoint, params={
        'param': random.randint(1, 10)
    }).json()

    # POST
    response_post = requests.post(endpoint, json={
        'jsonParam': random.randint(1, 10)
    }).json()

    # DELETE
    response_delete = requests.delete(endpoint).json()

    # вычисление результата
    total = response_get['number']

    total = execute_op(total, response_post['number'], response_post['operation'])
    total = execute_op(total, response_delete['number'], response_delete['operation'])

    print('Ответы сервера:')
    print(response_get)
    print(response_post)
    print(response_delete)

    print('Итоговое значение:', int(total))


# запуск
if __name__ == '__main__':
    Thread(target=lambda: app.run(debug=False, use_reloader=False)).start()
    time.sleep(1)
    run_client()

    

