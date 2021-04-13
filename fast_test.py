from requests import post, get, delete


print(post('http://127.0.0.1:8080/api/v2/users', json={
            "surname": 'zahar',
            "name": 'mark',
            "age": 17,
            "position": 1,
            "speciality": 'pupil',
            "address": 'mars',
            "email": '1@1',
            "hashed_password": '123'
}).json())
print(post('http://127.0.0.1:8080/api/v2/jobs', json={
            "team_leader": 1,
            "job": 'Hello world',
            "work_size": 17,
            "collaborators": 1,
            "start_date": 2,
            "end_date": 23,
            "is_finished": True,
}).json())
print(get('http://127.0.0.1:8080/api/v2/users').json())
print(delete('http://127.0.0.1:8080/api/v2/users/1').json())


print(get('http://127.0.0.1:8080/api/v2/jobs').json())
print(delete('http://127.0.0.1:8080/api/v2/jobs/1').json())


