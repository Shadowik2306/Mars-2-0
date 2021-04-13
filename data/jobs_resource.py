from flask_restful import reqparse, abort, Resource
from . import db_session
from .job import Jobs
from flask import jsonify


def abort_if_job_not_found(job_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Jobs).get(job_id)
    if not user:
        abort(404, message=f'User {job_id} not found')


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True, type=int)
parser.add_argument('end_date', required=True, type=int)
parser.add_argument('is_finished', required=True, type=bool)


class JobResource(Resource):
    def get(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(jobs_id)
        return jsonify({
            'jobs': job.to_dict()
        })

    def delete(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(jobs_id)
        db_sess.delete(job)
        db_sess.commit()
        return jsonify({
            'success': 'OK'
        })


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).all()
        return jsonify({
            'jobs': [item.to_dict() for item in job]
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args["job"],
            work_size=args["work_size"],
            collaborators=args["collaborators"],
            start_date=args["start_date"],
            end_date=args["end_date"],
            is_finished=args["is_finished"]
        )
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})



