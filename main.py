from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from data import db_session
from data.user import RegisterForm
from data.login_form import LoginForm
from data import main_api
from flask_ngrok import run_with_ngrok
from data.New import New_Coment
from data.coment import AddComForm
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
in_login = False
name = ''
com_form = []


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def menu():
    global in_login
    com_form = []
    ids = []
    db_sess = db_session.create_session()
    news = db_sess.query(New_Coment.id).all()
    for i in news:
        ids.append(*i)
    ids.reverse()
    ids = ids[:3]
    for i in range(3):
        news = db_sess.query(New_Coment.content).filter(New_Coment.id == ids[i]).first()
        news1 = db_sess.query(New_Coment.user_id).filter(New_Coment.id == ids[i]).first()
        com_form.append((*news, *news1))
    if in_login:
        return render_template('in_login/index2_0.html', title=com_form[0][0], title1=com_form[0][1],
                               title2=com_form[1][0], title3=com_form[1][1],
                               title4=com_form[2][0], title5=com_form[2][1])
    return render_template('index.html', title=com_form[0][0], title1=com_form[0][1],
                           title2=com_form[1][0], title3=com_form[1][1],
                           title4=com_form[2][0], title5=com_form[2][1])


@app.route('/logout')
@login_required
def log_out():
    logout_user()
    global in_login
    global name
    name = ''
    in_login = False
    return redirect("/")


@app.route('/menu2_0')
def menu2_0():
    return render_template('in_login/index2_0.html')


@app.route('/avia')
def avia():
    global in_login
    if in_login:
        return render_template('in_login/Avia.html')
    return render_template('Avia.html')


@app.route('/top')
def top():
    global in_login
    if in_login:
        return render_template('in_login/top.html')
    return render_template('top.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            global in_login
            in_login = True
            global name
            name = user.name
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.register_blueprint(main_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_session.global_init("db/mars_explorer.sqlite")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addcoment', methods=['GET', 'POST'])
def addcoment():
    global in_login
    global name
    if in_login:
        user = User()
        add_form = AddComForm()
        if add_form.validate_on_submit():
            db_sess = db_session.create_session()
            jobs = New_Coment(
                content=add_form.content.data,
                user_id=name
            )
            db_sess.add(jobs)
            db_sess.commit()
            return redirect("/")
        return render_template('in_login/addcoment.html', title='Adding a job', form=add_form)
    else:
        return redirect("/login")


if __name__ == '__main__':
    main()