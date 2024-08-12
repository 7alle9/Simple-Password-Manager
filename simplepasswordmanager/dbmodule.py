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


def signup(credentials):
    body = {'credentials': credentials}
    response = requests.post(settings.SIGNUP_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']


def add_new_password(credentials, key, password):
    body = {'credentials': credentials, 'key': key, 'password': password}
    response = requests.post(settings.ADD_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']


def update_password(credentials, key, password):
    body = {'credentials': credentials, 'key': key, 'password': password}
    response = requests.post(settings.UPDATE_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']


def delete_password(credentials, key):
    body = {'credentials': credentials, 'key': key}
    response = requests.post(settings.DELETE_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']


def change_master_password(credentials, new_password, passwords):
    body = {'credentials': credentials, 'new_password': new_password, 'passwords': passwords}
    response = requests.post(settings.CHANGE_MASTER_URL, json=body)
    is_success = response.json()['status'] == 'success'
    return is_success, response.json()['message']
