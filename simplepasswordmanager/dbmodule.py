import requests
import settings


def get_user_data(credentials):
    body = {'credentials': credentials}
    response = requests.post(settings.FETCH_URL, json=body)
    is_success = response.json()['status'] == 'success'
    if is_success:
        return True, response.json()['data']
    return False, response.json()['message']


def login(credentials):
    body = {'credentials': credentials}
    response = requests.post(settings.LOGIN_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']

print("Testing dbmodule", login({'username': '7alle9', 'password': '123456'}))