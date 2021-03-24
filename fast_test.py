from data.job import Jobs
from data import db_session
from data.users import User
from data.department import Department
from data.job import Jobs


db_session.global_init(input())
db_sess = db_session.create_session()
depart = db_sess.query(Department).filter(Department.id == 1).all()
