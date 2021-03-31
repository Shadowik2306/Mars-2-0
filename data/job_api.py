import flask

from . import db_session
from .job import Jobs
from flask import request, make_response, jsonify


db_session.global_init('db/blogs.db')



blueprint = flask.Blueprint(
    "jobs_api",
    __name__,
    template_folder='templates'
)

@blueprint.route('/api/jobs')
def get_job():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict() for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': "Not found"})
    return jsonify(
        {
            'jobs': [jobs.to_dict()]
        }
    )

@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'user', "job", "work_size",
                  'collaborators', 'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Jobs(
        team_leader=request.json['team_leader'],
        user=request.json['user'],
        job=request.json['job'],
        collaborators=request.json['collaborators'],
        work_size=request.json['work_size'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished'],
    )
    db_sess.add(job)
    db_sess.commit()

    return jsonify({'success': 'Ok'})
