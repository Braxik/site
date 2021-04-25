from flask import jsonify, render_template, redirect, request
import flask
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .users import User
from collections import defaultdict
from . import db_session
from .New import New_Coment
in_login = False
name = ''
blueprint = flask.Blueprint(
    'main_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/login', methods=['GET', 'POST'])
def login():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['email', 'password']):
        return jsonify({'error': 'Bad request'})
    form = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == form['email']).first()
    if user and user.check_password(form.password.data):
            login_user(user)
            global in_login
            in_login = True
            global name
            name = user.name
            try:
                print(current_user)
            except Exception:
                print('no')
            return jsonify({'success': 'OK'})
    else:
        return jsonify({'error': 'Wrong password'})


@blueprint.route('/api/take_com')
def three_com():
    com_form = []
    dictt = defaultdict(list)
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
    for i in com_form:
        a = i[1]
        b = i[0]
        dictt[a].append(b)
    print(dictt)
    return jsonify(
        {
            'new_com':
                [dictt]
        }
    )


@blueprint.route('/api/take_com/<int:id>', methods=['GET'])  # начинается с 16
def get_one_com(id):
    db_sess = db_session.create_session()
    news = db_sess.query(New_Coment).get(id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=('content', 'user_id'))
        }
    )


@blueprint.route('/api/com', methods=['POST'])
def coment():
    global in_login
    global name
    try:
        if True:
            print('iii')
    except Exception:
        return jsonify({'error': 'please log in'})
    try:
        if not request.json:
            return jsonify({'error': 'Empty request'})
        elif not all(key in request.json for key in
                     ['content']):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        news = New_Coment(
            content=request.json['content'],
            user_id=name
        )
        db_sess.add(news)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    except Exception:
        return jsonify({'error': 'please log in'})