import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__, template_folder='../templates')

#Адреса микросервисов
CURRENCY_MANAGER_URL = 'http://localhost:5001'
DATA_MANAGER_URL = 'http://localhost:5002'


#Главная страница
@app.route('/')
def index():
    return render_template('index.html')


#Прокси для currency-manager
@app.route('/api/load', methods=['POST'])
def proxy_load():
    resp = requests.post(f'{CURRENCY_MANAGER_URL}/load', json=request.get_json())
    return jsonify(resp.json()), resp.status_code


@app.route('/api/update_currency', methods=['POST'])
def proxy_update():
    resp = requests.post(f'{CURRENCY_MANAGER_URL}/update_currency', json=request.get_json())
    return jsonify(resp.json()), resp.status_code


@app.route('/api/delete', methods=['POST'])
def proxy_delete():
    resp = requests.post(f'{CURRENCY_MANAGER_URL}/delete', json=request.get_json())
    return jsonify(resp.json()), resp.status_code


#Прокси для data-manager
@app.route('/api/convert', methods=['GET'])
def proxy_convert():
    resp = requests.get(f'{DATA_MANAGER_URL}/convert', params=request.args)
    return jsonify(resp.json()), resp.status_code


@app.route('/api/currencies', methods=['GET'])
def proxy_currencies():
    resp = requests.get(f'{DATA_MANAGER_URL}/currencies')
    return jsonify(resp.json()), resp.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    