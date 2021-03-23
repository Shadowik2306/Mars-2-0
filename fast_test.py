from data.job import Jobs
from data import db_session
from data.users import User
from data.job import Jobs


db_session.global_init(input())
db_sess = db_session.create_session()
l = max([len(i.collaborators) for i in db_sess.query(Jobs).all()])
for job in db_sess.query(Jobs).filter(Jobs.collaborators.like('_' * l)).all():
    print(job.id.name)