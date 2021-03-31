from requests import get, post


print(post('http://127.0.0.1:8082/api/jobs',
    json={
        'id': 1,
        'job': 'Hello Mars',
        'team_leader': 1,
        'work_size': 20,
        'collaborators': '1, 2',
        'is_finished': True}).json())
print(post('http://127.0.0.1:8082/api/jobs',
    json={
        'id': 9999,
        'job': 'Hello Mars',
        'team_leader': '1',
        'work_size': 20,
        'collaborators': '1, 2',
        'is_finished': True}).json()) #правильное
print(post('http://127.0.0.1:8082/api/jobs',
    json={
        'job': 'Hello Mars',
        'work_size': 20,
        'collaborators': '1, 2',
        'is_finished': True}).json())
print(post('http://127.0.0.1:8082/api/jobs').json())

