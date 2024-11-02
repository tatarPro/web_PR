from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
@app.route("/")
@app.route("/base")
def index():
    user = "Студент СПК"
    return render_template('base.html', title='Домашняя страница', username=user)

@app.route("/training_mage")
def index1():
    user = "Студент СПК"
    return render_template('train.html', title='Тренировка', username=user)

@app.route("/training_cook")
def index2():
    user = "Студент СПК"
    return render_template('train2.html', title='Тренировка', username=user)

@app.route("/training_tailor")
def index3():
    user = "Студент СПК"
    return render_template('train3.html', title='Тренировка', username=user)

@app.route("/training_bard")
def index4():
    user = "Студент СПК"
    return render_template('train4.html', title='Тренировка', username=user)

@app.route("/training_melee")
def index5():
    user = "Студент СПК"
    return render_template('train5.html', title='Тренировка', username=user)

@app.route("/training_archer")
def index6():
    user = "Студент СПК"
    return render_template('train6.html', title='Тренировка', username=user)

@app.route("/training_horserider")
def index7():
    user = "Студент СПК"
    return render_template('train7.html', title='Тренировка', username=user)

@app.route("/list")
def index8():
    user = "Студент СПК"
    return render_template('list.html', title='Тренировка', username=user)

@app.route("/login")
def index9():
    user = "Студент СПК"
    return render_template('login.html', title='Тренировка', username=user)

@app.route("/distribution")
def index10():
    user = "Студент СПК"
    return render_template('distribution.html', title='Тренировка', username=user)

@app.route("/galery")
def index11():
    user = "Студент СПК"
    return render_template('galery.html', title='Тренировка', username=user)

@app.route("/auto_answer")
def index12():
    user = "Студент СПК"
    return render_template('auto_answer.html', title='Тренировка', username=user)

@app.route("/asist")
def index13():
    user = "Студент СПК"
    return render_template('asist.html', title='Тренировка', username=user)

@app.route("/guide")
def index14():
    user = "Студент СПК"
    return render_template('guide.html', title='Тренировка', username=user)

@app.route("/hero")
def index15():
    user = "Студент СПК"
    return render_template('hero.html', title='Тренировка', username=user)

@app.route("/items")
def index16():
    user = "Студент СПК"
    return render_template('items.html', title='Тренировка', username=user)

@app.route("/map")
def index17():
    user = "Студент СПК"
    return render_template('map.html', title='Тренировка', username=user)

@app.route("/oldanthem")
def index18():
    user = "Студент СПК"
    return render_template('oldanthem.html', title='Тренировка', username=user)

@app.route("/oldbase")
def index19():
    user = "Студент СПК"
    return render_template('oldbase.html', title='Тренировка', username=user)

@app.route("/rest")
def index20():
    user = "Студент СПК"
    return render_template('rest.html', title='Тренировка', username=user)



# Настройки базы данных SQLite (или можно использовать другую СУБД)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель данных для пользователей
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    education = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    motivation = db.Column(db.Text, nullable=False)
    ready_to_stay = db.Column(db.Boolean, default=False)
    news = db.relationship('News', backref='author', lazy=True)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Создать таблицы в базе данных (выполнить один раз)
with app.app_context():
    db.create_all()

# Главная страница с регистрационной формой
@app.route('/volunteers', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        surname = request.form['surname']
        name = request.form['name']
        education = request.form['education']
        profession = request.form['profession']
        gender = request.form['gender']
        motivation = request.form['motivation']
        ready_to_stay = 'ready_to_stay' in request.form

        # Создание нового пользователя
        new_user = User(
            surname=surname,
            name=name,
            education=education,
            profession=profession,
            gender=gender,
            motivation=motivation,
            ready_to_stay=ready_to_stay
        )

        # Добавление пользователя в базу данных
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/auto_answer')  # Перенаправление после успешной регистрации
        except:
            return 'Ошибка при добавлении данных в базу'

    return render_template('volunteers.html')

@app.route('/news', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = request.form['author_id']  # ID волонтера, выбранного из списка

        # Создание и добавление новости
        new_news = News(title=title, content=content, author_id=author_id)
        db.session.add(new_news)
        db.session.commit()
        return redirect(url_for('news'))

    # Получение всех новостей и волонтеров для формы
    all_news = News.query.order_by(News.date_posted.desc()).all()
    volunteers = User.query.all()
    return render_template('news.html', news=all_news, volunteers=volunteers)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')