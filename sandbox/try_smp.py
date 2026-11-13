# 探针脚本

from lib.device_model_api import list_device_models, add_device_model, del_device_model, get_device_id_list
from lib.login_api import login
import pytest
from lib.service_rule_api import add_service_rule, list_service_rule, get_service_rule_id, del_service_rule
import json

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsInVzZXJuYW1lIjoiYnloeSIsImV4cCI6MTc5NDcwMTc3N30.XRRkoelZiUE11-zpMzgmjLc7gNy4enYAdhouxKPdVFM'

import pytest
from lib.service_rule_api import *

# resp = del_service_rule(token, 1234567)
# del_data = resp.json()
# assert del_data['ret'] != 0

def test_service_rule_001_delete_existing(token, ser_cleaner, add_ser_data_test):
    new_id = add_ser_data_test()

    resp = del_service_rule(token, new_id)
    del_data = resp.json()
    assert del_data['ret'] == 0

    id_list_after = get_service_rule_id(token)
    assert new_id not in id_list_after




# resp = login('byhy', None)
# print(resp.status_code)
# data = resp.json()
# print(data)
# assert data['ret'] == 0
# assert 'token' in data



# name = '规则名称001 测试数据,预付费-下发业务量'
# rule_type_id = 1
# charge_rule = {
#                   'minFee':15,
#                   'estFee':50,
#                   'feeRates':[
#                       {
#                           'svcCode':'',
#                           'unitName':'度',
#                           'unitPrice':'1.3',
#
#                       }
#                   ]
#               }
# charge_rule = json.dumps(charge_rule)
# desc = '这是规则描述这是规则描述'
#
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEsInVzZXJuYW1lIjoiYnloeSIsImV4cCI6MTc5NDcwMTc3N30.XRRkoelZiUE11-zpMzgmjLc7gNy4enYAdhouxKPdVFM'
#
# add_resp = add_service_rule(token, name, rule_type_id, charge_rule, desc)
# add_data = add_resp.json()
# print(add_data)
# assert add_data['ret'] == 0
# new_id = add_data['id']
# # ser_cleaner.append(new_id)
#
# id_list = get_service_rule_id(token)
# assert new_id in id_list
#
# resp = del_service_rule(token, new_id)
# del_data = resp.json()
# assert del_data['ret'] == 0
#
# id_list_after = get_service_rule_id(token)
# assert new_id not in id_list_after







# 先拿 token
# resp = login('byhy', 'sdfsdf')
# token = resp.json()['token']
#
# del_resp = del_device_model(token, 10000)
# del_data = del_resp.json()
# assert del_data['ret'] == 0
#
# id_list_after = get_device_id_list(token)
# new_id = 10000
# print(f'目前存在的所有id：{id_list_after}')
# assert new_id not in id_list_after

# # 新增一条，拿到真实 id
# add_resp = add_device_model(token, 3, "probe_tmp_01", "探针临时数据")
# add_json = add_resp.json()
# print("新增返回：", add_json)
# tmp_id = add_json["id"]
#
# # 尝试删除这条刚刚新增的
# del_resp = del_device_model(token, tmp_id)
# del_json = del_resp.json()
# print("删除返回：", del_json)
#
# # 查询确认
# ids = get_device_id_list(token)
# print("现在列表里面所有 id：", ids)
# print(f"{tmp_id} 是否在列表：{tmp_id in ids}")
#
# # 再删一次 / 删一个不存在 id，探边界
# print("\n--- 尝试删除不存在 id：9999999 ---")
# resp = del_device_model(token, 9999999)
# print(resp.json())



