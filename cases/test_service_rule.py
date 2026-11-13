# cases/test_service_rule.py

import pytest
from lib.service_rule_api import *


# 增删查全流程
@pytest.mark.parametrize(
    'name, rule_type_id, args, desc, type_name',
    [
        (
            '规则名称001 测试数据',
            1,
            (15,50,'','度','1.3'),
            '这是规则描述这是规则描述',
            'prepaid_volume'
        ),
        (
            '规则名称002 测试数据',
            2,
            (2,3),
            '这是规则描述这是规则描述',
            'prepaid_fee'
        ),
        (
            '规则名称003 测试数据',
            3,
            ([(1,2,3),(4,5,6),(7,8,9)],),
            '这是规则描述这是规则描述',
            'postpaid'
        )
    ]
)
def test_service_rule_001_full_flow(token, ser_cleaner, name, rule_type_id, args, desc, type_name):
    charge_rule = build_charge_rule_by_type(type_name, args)

    add_resp = add_service_rule(token, name, rule_type_id, charge_rule, desc)
    add_data = add_resp.json()
    assert add_data['ret'] == 0
    new_id = add_data['id']
    ser_cleaner.append(new_id)

    id_list = get_service_rule_id(token)
    assert new_id in id_list

    resp = del_service_rule(token, new_id)
    del_data = resp.json()
    assert del_data['ret'] == 0

    id_list_after = get_service_rule_id(token)
    assert new_id not in id_list_after

# 新增正常数据
def test_service_rule_002_add_normal(token, ser_cleaner):
    charge_rule = build_charge_rule_by_type('prepaid_volume', (55,66,'','磅','0.23'))

    add_resp = add_service_rule(token, '规则名称1 测试数据', 1, charge_rule, '描述描述')
    add_data = add_resp.json()
    assert add_data['ret'] == 0
    new_id = add_data['id']
    ser_cleaner.append(new_id)

    id_list = get_service_rule_id(token)
    assert new_id in id_list

# 新增不存在的type_id的数据
@pytest.mark.xfail(reason='后端缺少type_id校验，错误数据当前可正常入库，待修复')
def test_service_rule_003_add_invalid_typeid(token, ser_cleaner):
    charge_rule = build_charge_rule_by_type('prepaid_volume', (55, 66, '', '磅', '0.23'))

    add_resp = add_service_rule(token, '规则名称4 测试数据', 4, charge_rule, '描述描述')
    add_data = add_resp.json()
    if 'id' in add_data:
        new_id = add_data['id']
        ser_cleaner.append(new_id)

    assert add_data['ret'] != 0

# 关键词过滤
def test_service_rule_004_keywords_filter(token, ser_cleaner):
    name = '关键词过滤abcdddd@#$%^'
    charge_rule = build_charge_rule_by_type('prepaid_volume', (55, 66, '', '磅', '0.23'))
    add_resp = add_service_rule(token, name, 1, charge_rule, '描述描述')
    add_data = add_resp.json()
    new_id = add_data['id']
    ser_cleaner.append(new_id)

    # 存在关键词
    resp_match = list_service_rule(token, keywords='abcdddd')
    data_match = resp_match.json()
    assert  data_match['ret'] == 0
    assert any(item['name'] == name for item in data_match['retlist'])

    # 不存在关键词
    resp_match2 = list_service_rule(token, keywords='绝对不存在的词zzz')
    data_match2 = resp_match2.json()
    assert data_match2['ret'] == 0
    assert data_match2['retlist'] == []

# 删除存在的数据
def test_service_rule_005_delete_existing(token, ser_cleaner, add_ser_data_test):
    new_id = add_ser_data_test

    resp = del_service_rule(token, new_id)
    del_data = resp.json()
    assert del_data['ret'] == 0

    id_list_after = get_service_rule_id(token)
    assert new_id not in id_list_after

# 删除不存在的数据
@pytest.mark.xfail(reason='后端缺少删除不存在id校验，不存在数据当前可正常删除，待修复')
def test_service_rule_006_delete_non_exist(token):
    resp = del_service_rule(token, 1234567)
    del_data = resp.json()
    assert del_data['ret'] != 0