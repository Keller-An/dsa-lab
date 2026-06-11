import json
import os
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Настройка ограничителя запросов
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://"
)

# Имя файла для хранения данных
DATA_FILE = "data.json"

# Загрузка данных из файла при старте приложения
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Сохранение данных в файл
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Глобальный словарь-хранилище
data_store = load_data()

#Маршруты

@app.route("/set", methods=["POST"])
@limiter.limit("10 per minute")  
def set_key():
    """Сохранить ключ-значение"""
    content = request.get_json()
    if not content:
        return jsonify({"error": "Ожидается JSON"}), 400
    
    key = content.get("key")
    value = content.get("value")
    
    if key is None or value is None:
        return jsonify({"error": "Требуются поля 'key' и 'value'"}), 400
    
    data_store[key] = value
    save_data(data_store)
    return jsonify({"status": "ok", "message": f"Ключ '{key}' сохранён"}), 200


@app.route("/get/<string:key>", methods=["GET"])
def get_key(key):
    """Получить значение по ключу"""
    value = data_store.get(key)
    if value is None:
        return jsonify({"error": f"Ключ '{key}' не найден"}), 404
    return jsonify({"key": key, "value": value}), 200


@app.route("/delete/<string:key>", methods=["DELETE"])
@limiter.limit("10 per minute")  # отдельный лимит для /delete
def delete_key(key):
    """Удалить ключ"""
    if key not in data_store:
        return jsonify({"error": f"Ключ '{key}' не найден"}), 404
    
    del data_store[key]
    save_data(data_store)
    return jsonify({"status": "ok", "message": f"Ключ '{key}' удалён"}), 200


@app.route("/exists/<string:key>", methods=["GET"])
def exists_key(key):
    """Проверить наличие ключа"""
    exists = key in data_store
    return jsonify({"key": key, "exists": exists}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    