from flask import Flask, url_for, render_template, redirect, jsonify, make_response, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session, job_api, user_api, users_resource, jobs_resource
from data.users_resource import *
from data.users import User
from data.job import Jobs
from data.department import Department

from forms.loginForm import LoginForm
from forms.registrationForm import Register
from forms.addingJob import AddingJob
from forms.loginFormTwo import LoginFormTwo
from forms.depart import AddingDep

import datetime
import os
import requests
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/blogs.db')
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'})), 404


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def works_log():
    if not current_user.is_authenticated:
        return render_template('base.html')
    print(1)
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('works_log.html', jobs=jobs)


@app.route('/training/<prof>')
def training(prof):
    params = {}
    if 'строитель' in prof or 'инженер' in prof:
        params['prof_text'] = 'Инженерные тренажеры'
        params['prof_image'] = url_for('static', filename='img/doc_or_eng/eng.jpg')
    else:
        params['prof_text'] = 'Научные симуляторы'
        params['prof_image'] = url_for('static', filename='img/doc_or_eng/doc.jpg')
    return render_template('training.html', **params)


@app.route('/list_prof/<name>')
def list_prof(name):
    params = {
        'list': name,
        'lst_prof': ['инженер-исследователь', 'пилот', 'строитель',
                     'экзобиолог', 'врач', 'инженер по терраформированию',
                     'климатолог', 'специалист по радиационной защите',
                     'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения',
                     'метеоролог', 'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов']
    }
    return render_template('list_prof.html', **params)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    params = {'info': {
        'title': 'HAHAHA',
        'surname': 'Zahar',
        'name': 'Mark',
        'education': 'NO EDU',
        'profession': 'programmer',
        'sex': 'only with bugs',
        'motivation': 'YES',
        'ready': 'Maybe'
        }
    }
    return render_template('answer.html', **params)


@app.route('/login_two', methods=['GET', 'POST'])
def login_two():
    form = LoginFormTwo()
    if form.validate_on_submit():
        return redirect('/#')
    return render_template('login_two.html', title='Аварийный доступ', form=form)


@app.route('/distribution')
def distribution():
    lst = ['A', 'B', 'C', 'D']
    return render_template('distribution.html', lst=lst)


@app.route('/table_param/<name>/<int:age>')
def table_prof(name, age):
    if name == 'male':
        if age > 21:
            color = '#23037C'
        else:
            color = '#571DFC'
    else:
        if age < 21:
            color = '#FF6BEF'
        else:
            color = '#E506C2'
    return render_template('table_param.html', color=color,
                           name=url_for('static', filename='img/sim/male_child.jpg'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        if not form.password.data == form.password_repeat.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', form=form,
                                   message="Такой пользователь уже есть")
        new_user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.login.data,
            age=form.age.data,
            address=form.address.data,
            position=form.position.data,
            speciality=form.speciality.data,
            modified_date=datetime.datetime.now()
        )
        new_user.set_password(form.password.data)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/news', methods=['GET', "POST"])
@login_required
def addjob():
    form = AddingJob()
    if form.validate_on_submit():
        new_job = Jobs(
            team_leader=form.team_led_id.data,
            job=form.title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.finished.data
        )
        db_sess = db_session.create_session()
        db_sess.add(new_job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = AddingJob()
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter((Jobs.team_leader == id) | (current_user.id == 1)).first()
    if not news:
        return redirect('/')
    if form.validate_on_submit():
        news.team_leader = form.team_led_id.data
        news.job = form.title.data
        news.work_size = form.work_size.data
        news.collaborators = form.collaborators.data
        news.is_finished = form.finished.data
        db_sess.commit()
        return redirect('/')
    form.title.data = news.job
    form.team_led_id.data = news.team_leader
    form.work_size.data = news.work_size
    form.collaborators.data = news.collaborators
    form.finished.data = news.is_finished
    return render_template('addjob.html', title='Editing a job', form=form)


@app.route('/del_jobs/<int:id>', methods=['GET','POST'])
@login_required
def del_new(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter((Jobs.team_leader == id) | (current_user.id == 1)).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    return redirect('/')


@app.route('/depart_list', methods=['GET', 'POST'])
@login_required
def depart_list():
    db_session.global_init('db/blogs.db')
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).all()
    return render_template('depart.html', departs=depart)


@app.route('/depart_list_add', methods=['GET', "POST"])
@login_required
def depAdd():
    form = AddingDep()
    if form.validate_on_submit():
        new_dep = Department(
            chief=form.chief.data,
            title=form.title.data,
            members=form.members.data,
            email=form.email.data
        )
        db_sess = db_session.create_session()
        db_sess.add(new_dep)
        db_sess.commit()
        return redirect('/depart_list')

    return render_template('add_dep.html', title='Adding a job', form=form)


@app.route('/depart_list/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_edit(id):
    form = AddingDep()
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter((Department.chief == id) | (current_user.id == 1)).first()
    if not dep:
        return redirect('/depart_list')
    if form.validate_on_submit():
        dep.chief = form.chief.data
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        db_sess.commit()
        return redirect('/depart_list')
    form.title.data = dep.title
    form.chief.data = dep.chief
    form.members.data = dep.members
    form.email.data = dep.email

    return render_template('add_dep.html', title='Editing a job', form=form)


@app.route('/del_dep/<int:id>', methods=['GET','POST'])
@login_required
def del_dep(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Department).filter((Department.chief == id) | (current_user.id == 1)).first()
    if depart:
        db_sess.delete(depart)
        db_sess.commit()
    return redirect('/')


@app.route('/nostalgy', methods=['GET'])
@login_required
def nostalgy():
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": current_user.address,
        "format": 'json'
    }
    response = requests.get(geocoder_request, params=geocoder_params)
    if not response:
        abort(404)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
    toponym_cords = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_cords.split(" ")
    address_ll = toponym_longitude + ',' + toponym_lattitude
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": address_ll,
        "l": "map",
    }
    response = requests.get(map_api_server, params=map_params)
    with open(f'static/nostalgy/nostalgy_{current_user.email}.jpg', 'wb') as fd:
        fd.write(response.content)
    return render_template('nostalgy.html')


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    lst = ['static/img/galery/' + i for i in os.listdir('static/img/galery')]
    return render_template('galery.html', lst=lst)


@login_required
@app.route('/member')
def member():
    lst = ['static/img/galery/' + i for i in os.listdir('static/img/galery')]
    return render_template('member.html', jpg=random.choice(lst))


if __name__ == '__main__':
    app.register_blueprint(job_api.blueprint)
    app.register_blueprint(user_api.blueprint)
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:users_id>')
    api.add_resource(jobs_resource.JobResource, '/api/v2/jobs/<int:jobs_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs')
    app.run(port=8080, host='127.0.0.1')