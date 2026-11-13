# lib/service_rule_api.py
import json

import requests
from cfg import SMP_ADDRESS, SMP_URL_SERVICE_RULE, SMP_URL_SERVICE_RULE_DEL, SMP_URL_SERVICE_RULE_ADD


def list_service_rule(token, pagesize=5, pagenum=1, keywords=''):
    url = f'{SMP_ADDRESS}{SMP_URL_SERVICE_RULE}'
    headers = {'authorization':f'Bearer {token}'}
    params ={
        'pagesize':pagesize,
        'pagenum': pagenum,
        'keywords': keywords
    }

    resp = requests.get(url, headers=headers, params=params)
    return resp

def add_service_rule(token, name, rule_type_id, charge_rule, desc):
    url = f'{SMP_ADDRESS}{SMP_URL_SERVICE_RULE_ADD}'
    headers = {'authorization':f'Bearer {token}'}
    payload = {
        'charge_rule': json.dumps(charge_rule),
        'desc': desc,
        'name': name,
        'rule_type_id': rule_type_id
    }

    resp = requests.post(url, headers=headers, json=payload)
    return resp

def del_service_rule(token, ser_id):
    url = f'{SMP_ADDRESS}{SMP_URL_SERVICE_RULE_DEL}'
    headers = {'authorization':f'Bearer {token}'}
    payload = {'id':ser_id}

    resp = requests.delete(url, headers=headers, json=payload)
    return resp

def get_service_rule_id(token, pagesize=100, pagenum=1, keywords=''):
    list_resp = list_service_rule(token, pagesize=100, pagenum=1, keywords='')
    list_data = list_resp.json()
    assert list_data['ret'] == 0

    id_list = [item['id'] for item in list_data['retlist']]
    return id_list

# 1.预付费-下发业务量 charge_rule 构造函数
def build_service_rule_prepaid_volume(minFee, estFee, svcCode, unitName, unitPrice):
    d = {
        'minFee':minFee,
        'estFee':estFee,
        'feeRates':[{
            'svcCode':svcCode,
            'unitName':unitName,
            'unitPrice':unitPrice}]
    }
    return d

# 2.预付费-下发费用 charge_rule 构造函数
def build_service_rule_prepaid_fee(minFee, estFee):
    d = {
        'minFee':minFee,
        'estFee':estFee
    }
    return d

# 3.后付费-上报业务量 charge_rule 构造函数
def build_service_rule_postpaid(fee_list):
    d = {
        'feeRates':[
            {
                'svcCode':svcCode,
                'unitName':unitName,
                'unitPrice':unitPrice
            }
            for svcCode,unitName,unitPrice in fee_list
        ]
    }
    return d

# 用'type_name'来判断使用哪个构造函数
def build_charge_rule_by_type(type_name, args):
    if type_name == 'prepaid_volume':
        charge_rule = build_service_rule_prepaid_volume(*args)
    elif type_name == 'prepaid_fee':
        charge_rule = build_service_rule_prepaid_fee(*args)
    elif type_name == 'postpaid':
        charge_rule = build_service_rule_postpaid(*args)
    else:
        raise ValueError('未知规则类型')
    return charge_rule