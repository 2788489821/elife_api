# conftest.py

import pytest
from lib.device_model_api import add_device_model, del_device_model
from lib.login_api import login
from lib.service_rule_api import del_service_rule, add_service_rule, build_charge_rule_by_type


# 获取token
@pytest.fixture(scope='module')
def token():
    resp = login('byhy','sdfsdf')
    data = resp.json()
    assert data['ret'] == 0

    yield data['token']

# 新增一条临时device数据并获取id，用完后自动删除
@pytest.fixture()
def add_dev_data_test(token):
    add_resp = add_device_model(token, 3, 'probe_tmp_01', '探针临时数据')
    add_json = add_resp.json()
    print(f'新增临时数据：{add_json}')
    new_id = add_json['id']

    yield new_id

    # 再写一遍删除以确保删除成功
    try:
        del_device_model(token, new_id)
    except Exception:
        pass

# 新增一条临时service数据并获取id，用完后自动删除
@pytest.fixture()
def add_ser_data_test(token):
    charge_rule = build_charge_rule_by_type('prepaid_fee', (1,2))
    add_resp = add_service_rule(token, '规则名称002 测试数据',2, charge_rule,'探针临时数据')
    add_json = add_resp.json()
    print(f'新增临时数据：{add_json}')
    new_id = add_json['id']

    yield new_id

    # 再写一遍删除以确保删除成功
    try:
        del_service_rule(token, new_id)
    except Exception:
        pass

# 还原新增的数据
@pytest.fixture
def dev_cleaner(token):
    id_list = []

    yield id_list

    for added_id in id_list:
        try:
            del_device_model(token, added_id)
        except Exception:
            pass

# 还原新增的数据
@pytest.fixture
def ser_cleaner(token):
    id_list = []

    yield id_list

    for added_id in id_list:
        try:
            del_service_rule(token, added_id)
        except Exception:
            pass