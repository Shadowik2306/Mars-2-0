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