from requests import get, post, delete


print(delete('http://127.0.0.1:8082/api/jobs/2').json())

