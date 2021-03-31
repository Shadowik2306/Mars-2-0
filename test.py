from requests import get, post


print(get('http://127.0.0.1:8080/api/jobs').json())
print(get('http://127.0.0.1:8080/api/jobs/1').json())
print(get('http://127.0.0.1:8080/api/jobs/999').json())
print(get('http://127.0.0.1:8080/api/jobs/helloWorld').json())
print(post('http://127.0.0.1:8080/api/jobs').json())