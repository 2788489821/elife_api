# lib/api_smp.py

import requests
from cfg import SMP_ADDRESS, PATH_Device_Model

def login(username, password):
    url = f'{SMP_ADDRESS}/api/operator_login'

    resp = requests.post(url, json={'username': username, 'password': password})
    return resp

def list_device_models(token, pagesize=5,pagenum=1,keywords=''):
    url = f'{SMP_ADDRESS}{PATH_Device_Model}'
    resp = requests.get(url,
                        headers={'Authorization':'Bearer '+token},
                        params={
                            'pagesize':pagesize,
                            'pagenum':pagenum,
                            'keywords': keywords
                        }
                        )
    return resp
