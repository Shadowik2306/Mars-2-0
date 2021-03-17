from flask import Flask, url_for, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


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



if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')