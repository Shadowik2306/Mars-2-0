from requests import get, post, delete, put


print(delete('http://127.0.0.1:8082/api/user/2').json())

print(post('http://127.0.0.1:8082/api/user', json={
    'surname': 'Zahar',
    'name': 'Mark',
    'age': 17,
    'position': 'Mars',
    'speciality': 'Pupil',
    'address': 'DarkWeb',
    'email': 'Nope',
    'hashed_password': '12345'

}).json())

print(put('http://127.0.0.1:8082/api/user/2', json={
    'email': 'hello@world.ru'
}).json())

