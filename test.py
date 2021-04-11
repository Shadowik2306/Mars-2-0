from requests import get, post, delete, put


print(get('http://127.0.0.1:8082/api/v2/users').json())

