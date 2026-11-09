# lib/api_smp.py

import requests
from cfg import *


def login(username, password):
    url = f'{SMP_ADDRESS}{SMP_URL_LOGIN}'

    resp = requests.post(url, json={'username': username, 'password': password})
    return resp

def list_device_models(token, pagesize=5, pagenum=1, keywords=''):
    url = f'{SMP_ADDRESS}{SMP_URL_DEVICE_MODEL}'
    headers = {'Authorization':'Bearer '+token}
    params = {
        'pagesize': pagesize,
        'pagenum': pagenum,
        'keywords': keywords
    }
    resp = requests.get(url, headers=headers, params=params)
    return resp

def add_device_model(token, typeid, name, desc):
    url = f'{SMP_ADDRESS}{SMP_URL_DEVICE_MODEL_ADD}'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {
        'typeid':typeid,
        'name':name,
        'desc':desc
    }
    resp = requests.post(url, headers=headers, json=payload)
    return resp

def del_device_model(token, dev_id):
    url = f'{SMP_ADDRESS}{SMP_URL_DEVICE_MODEL_DEL}'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'id':dev_id}
    resp = requests.delete(url, headers=headers, json=payload)
    return resp