from data.job import Jobs
from data import db_session
from data.users import User
from data.department import Department
from data.job import Jobs


db_session.global_init(input())
db_sess = db_session.create_session()
depart = db_sess.query(Department).filter(Department.id == 1).one()
lst = [int(i) for i in depart.members.split(', ')]
dct = {str(i): 0 for i in lst}
for i in dct.keys():
    users = [(list(map(int, j.collaborators.split(', '))), j.work_size) for j in db_sess.query(Jobs).all()]
    for peaple in users:
        if int(i) in peaple[0]:
            dct[i] += peaple[1]
for key, value in dct.items():
    if value < 25:
        continue
    user = db_sess.query(User).filter(User.id == int(key)).one()
    print(user.surname, user.name)


