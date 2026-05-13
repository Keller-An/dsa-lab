import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'currency_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}


def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn


#Конвертация
@app.route('/convert', methods=['GET'])
def convert_currency():
    currency_name = request.args.get('currency_name')
    amount = request.args.get('amount')

    if not currency_name or not amount:
        return jsonify({'error': 'currency_name и amount обязательны'}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'amount должен быть числом'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    #Проверка существования валюты
    cur.execute('SELECT rate FROM currencies WHERE currency_name = %s', (currency_name,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return jsonify({'error': 'Валюта не найдена'}), 404

    rate = float(result['rate'])
    converted = amount * rate

    return jsonify({
        'currency': currency_name,
        'amount': amount,
        'rate': rate,
        'converted_to_rub': round(converted, 2)
    }), 200


#Возврат списка всех валют с курсами
@app.route('/currencies', methods=['GET'])
def get_all_currencies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, currency_name, rate FROM currencies ORDER BY id')
    currencies = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(currencies), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)