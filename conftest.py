# conftest.py

import pytest
from lib.device_model_api import add_device_model, del_device_model
from lib.login_api import login

# 获取token
@pytest.fixture(scope='module')
def token():
    resp = login('byhy','sdfsdf')
    data = resp.json()
    assert data['ret'] == 0

    yield data['token']

# 新增一条临时数据并获取id，用完后自动删除
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
