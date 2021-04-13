from requests import post, get, delete


print(post('http://127.0.0.1:8082/api/v2/users', json={
            "surname": 'zahar',
            "name": 'mark',
            "age": 17,
            "position": 1,
            "speciality": 'pupil',
            "address": 'mars',
            "email": '1@1',
            "hashed_password": '123'
}).json())
print(get('http://127.0.0.1:8082/api/v2/users').json())
print(delete('http://127.0.0.1:8082/api/v2/users/1'))