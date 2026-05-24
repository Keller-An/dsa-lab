from flask import Flask, request, jsonify, render_template, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from decimal import Decimal
import psycopg2
import requests

app = Flask(__name__)
app.secret_key = "secret_key"

#БД
conn = psycopg2.connect(
    dbname="finance_db",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


#Главная страница
@app.route("/")
def home():
    return redirect("/login")


#Регистрация
@app.route("/reg", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    try:
        data = request.get_json()
        name = data["name"]
        password = data["password"]

        cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
        if cursor.fetchone():
            return jsonify({"message": "Пользователь уже существует"}), 400

        hashed = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (name, password) VALUES (%s, %s)", (name, hashed)
        )
        conn.commit()

        return jsonify({"message": "Регистрация успешна"}), 200

    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({"message": "ERROR"}), 500


#Логин
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    name = request.form["name"]
    password = request.form["password"]

    if not name or not password:
        return "Заполните все поля", 400

    cursor.execute(
        "SELECT id, name, password, is_admin FROM users WHERE name = %s", (name,)
    )

    user = cursor.fetchone()

    if user and check_password_hash(user[2], password):

        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["is_admin"] = user[3]

        #Редирект 
        if user[3]:
            return redirect("/admin/users")
        else:
            return redirect("/operations")

    return "Неверный логин или пароль"


#Выход
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


#Добавление операций
@app.route("/add_operation", methods=["POST"])
def add_operation():

    if "user_id" not in session:
        return jsonify({"message": "Не авторизован"}), 401

    try:
        data = request.get_json()

        operation_type = data["type_operation"]
        operation_amount = data["amount"]
        operation_date = data["date"]

        cursor.execute(
            """
            INSERT INTO operations (date, amount, type_operation, user_id)
            VALUES (%s, %s, %s, %s)
            """,
            (operation_date, operation_amount, operation_type, session["user_id"])
        )

        conn.commit()

        return jsonify({"message": "Операция добавлена"}), 200

    except Exception as e:
        conn.rollback()
        print(e)
        return jsonify({"message": "ERROR"}), 500


#Операции
@app.route("/operations")
def operations():

    if "user_id" not in session:
        return redirect("/login")

    # админ не должен сюда попадать
    if session.get("is_admin"):
        return redirect("/admin/users")

    currency = request.args.get("currency", "RUB")
    rate = Decimal("1")

    if currency != "RUB":
        response = requests.get(
            "http://127.0.0.1:5001/rate",
            params={"currency": currency}
        )
        data = response.json()
        rate = Decimal(str(data["rate"]))

    cursor.execute(
        """
        SELECT id, date, amount, type_operation
        FROM operations WHERE user_id = %s
        ORDER BY date DESC
        """,
        (session["user_id"],)
    )

    rows = cursor.fetchall()

    result = []

    for row in rows:
        converted = round(row[2] / rate, 2)

        result.append({
            "id": row[0],
            "date": row[1],
            "amount": converted,
            "type": row[3]
        })

    return render_template(
        "operations.html",
        operations=result,
        currency=currency
    )


#Панель администратора
@app.route("/admin/users")
def admin_users():

    if not session.get("user_id"):
        return redirect("/login")

    if not session.get("is_admin"):
        return "Нет доступа", 403

    cursor.execute("SELECT id, name, is_admin FROM users ORDER BY id")
    users = cursor.fetchall()

    return render_template("admin_users.html", users=users)


#Удаление пользователя админом
@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    if not session.get("is_admin"):
        return "Нет доступа", 403

    cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        flash("Пользователь не найден")
        return redirect("/admin/users")

    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()

    flash("Пользователь успешно удалён")

    return redirect("/admin/users")


if __name__ == "__main__":
    app.run(debug=True)