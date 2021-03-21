from flask import Flask, url_for, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Label
from wtforms.validators import DataRequired
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    param = {}
    param['title'] = title
    return render_template('base.html', **param)


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


class LoginForm(FlaskForm):
    username_astro = StringField('id астронавта', validators=[DataRequired()])
    password_astro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    username_cap = StringField('id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/#')
    return render_template('login.html', title='Аварийный доступ', form=form)


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
    return render_template('table_param.html', color=color, name=url_for('static', filename='img/sim/male_child.jpg'))


class GaleryForm(FlaskForm):
    file = SubmitField('Выберите файл')
    send = SubmitField('Отправить')


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    if request.method == 'GET':
        form = GaleryForm()
        return render_template('galery.html', lst=[url_for('static', filename=f'img/galery/{i}') for i in os.listdir('static/img/galery')], form = form)
    elif request.method == 'POST':
        f = request.files['file']
        f.read()
        with open(str(os.listdir('static/img/galery')) + '.jpg', 'w') as file:
            file.write(f)


@app.route('/sample_file_upload', methods=['POST', 'GET'])
def sample_file_upload():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                             <link rel="stylesheet"
                             href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                             integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                             crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример загрузки файла</title>
                          </head>
                          <body>
                            <h1>Загрузим файл</h1>
                            <form method="post" enctype="multipart/form-data">
                               <div class="form-group">
                                    <label for="photo">Выберите файл</label>
                                    <input type="file" class="form-control-file" id="photo" name="file">
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        with open(str(os.listdir('static/img/galery')) +'.jpg', 'w') as file:
            file.write(f)
        return "Форма отправлена"

if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')