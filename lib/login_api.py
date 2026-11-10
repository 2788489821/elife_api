# lib/login_api.py

import requests
from cfg import *

def login(username, password):
    url = f'{SMP_ADDRESS}{SMP_URL_LOGIN}'

    resp = requests.post(url, json={'username': username, 'password': password})
    return resp