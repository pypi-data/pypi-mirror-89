import requests

URL = 'https://auth.dupl.tech/api'

def user(token: str) -> dict:
    r = requests.post(f'{URL}/user', data={
        'token': token,
    })
    return r.json()['user']