import flask
from . import db_session
from .users import User
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from datetime import datetime


db_session.global_init('db/blogs.db')


blueprint = flask.Blueprint(
    "user_api",
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'user': [item.to_dict() for item in user]
        }
    )


@blueprint.route('/api/user/<int:id>', methods=["GET"])
def get_one_user(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    if not user:
        return jsonify({'error': "Not found"})
    return jsonify(
        {
            'user': [user.to_dict()]
        }
    )

@blueprint.route('/api/user', methods=['POST'])
def post_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality',
                  'address', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        modified_date=datetime.now(),
        hashed_password=generate_password_hash(request.json['hashed_password'])
    )
    db_sess.add(user)
    db_sess.commit()

    return jsonify({'success': 'Ok'})


@blueprint.route('/api/user/<int:id>', methods=['DELETE'])
def del_user(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:id>', methods=['PUT'])
def change_job(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    if not users:
        return jsonify({'error': 'Not found'})
    try:
        users.surname = request.json['surname']
    except Exception:
        pass
    try:
        users.name = request.json['name']
    except Exception:
        pass
    try:
        users.age = request.json['age']
    except Exception:
        pass
    try:
        users.position = request.json['position']
    except Exception:
        pass
    try:
        users.speciality = request.json['speciality']
    except Exception:
        pass
    try:
        users.address = request.json['address']
    except Exception:
        pass
    try:
        users.email = request.json['email']
    except Exception:
        pass
    try:
        users.hashed_password = generate_password_hash(request.json['hashed_password'])
    except Exception:
        pass
    users.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'success': 'OK'})