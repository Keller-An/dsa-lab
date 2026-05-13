import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

#Подключение к PostgreSQL
DB_CONFIG = {
    'dbname': 'currency_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

#Создание и возврат соединения с БД
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    return conn


#Эндпоинт для добавления новой валюты
@app.route('/load', methods=['POST'])
def load_currency():
    data = request.get_json()
    currency_name = data.get('currency_name')
    rate = data.get('rate')

    if not currency_name or rate is None:
        return jsonify({'error': 'currency_name и rate обязательны'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    #Проверка, существует ли валюта
    cur.execute('SELECT id FROM currencies WHERE currency_name = %s', (currency_name,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'error': 'Валюта уже существует'}), 409

    #Сохранение валюты
    cur.execute(
        'INSERT INTO currencies (currency_name, rate) VALUES (%s, %s)',
        (currency_name, rate)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': f'Валюта {currency_name} успешно добавлена'}), 200


#Эндпоинт для обновления курса валюты.
@app.route('/update_currency', methods=['POST'])
def update_currency():
    data = request.get_json()
    currency_name = data.get('currency_name')
    rate = data.get('rate')

    if not currency_name or rate is None:
        return jsonify({'error': 'currency_name и rate обязательны'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    #Проверка существования валюты
    cur.execute('SELECT id FROM currencies WHERE currency_name = %s', (currency_name,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'error': 'Валюта не найдена'}), 404

    #Обновление курса
    cur.execute(
        'UPDATE currencies SET rate = %s WHERE currency_name = %s',
        (rate, currency_name)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': f'Курс валюты {currency_name} обновлён'}), 200


#Эндпоинт для удаления валюты
@app.route('/delete', methods=['POST'])
def delete_currency():
    data = request.get_json()
    currency_name = data.get('currency_name')

    if not currency_name:
        return jsonify({'error': 'currency_name обязателен'}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    #Проверка существования валюты
    cur.execute('SELECT id FROM currencies WHERE currency_name = %s', (currency_name,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({'error': 'Валюта не найдена'}), 404

    #Удаление валюты
    cur.execute('DELETE FROM currencies WHERE currency_name = %s', (currency_name,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': f'Валюта {currency_name} удалена'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

    