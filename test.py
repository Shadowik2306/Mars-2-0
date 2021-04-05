from requests import get, post, delete, put


print(put('http://127.0.0.1:8082/api/jobs/1', json={'job': 'Hello Mars'}).json())

