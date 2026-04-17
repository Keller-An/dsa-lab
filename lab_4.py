from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# БД
user_db = {}

class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name 

# Загрузка пользователя 
@login_manager.user_loader
def load_user(user_id):
    for user in user_db.values():
        if str(user.id) == str(user_id):
            return user
    return None


# Главная страница
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    else:
        return redirect(url_for('login'))
    

# Страница входа
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


# Авторизация
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Заполните все поля')
        return redirect(url_for('login'))
    
    user = user_db.get(email)

    if not user:
        flash('Пользователь не найден')
        return redirect(url_for('login'))
    
    if user.password != password:
        flash('Неверный пароль')
        return redirect(url_for('login'))
    
    #Вход на сайт
    login_user(user)
    return redirect(url_for('index'))


# Страница регистрации 
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


#Регистрация 
@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash('Все поля обязательны к заполнению')
        return redirect(url_for('signup'))
    
    if email in user_db:
        flash('Такой пользователь уже существует')
        return redirect(url_for('signup'))
    
    # Создание нового пользователя
    new_user = User(
        id=len(user_db) + 1,
        email=email,
        password=password,
        name=name
    )

    user_db[email] = new_user
    return redirect(url_for('login'))

#Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Запуск
if __name__ == '__main__':
    app.run(debug=True)