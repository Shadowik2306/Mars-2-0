from flask import Flask, url_for, render_template


app = Flask(__name__)


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



if __name__ == '__main__':
    app.run(port=8081, host='127.0.0.1')