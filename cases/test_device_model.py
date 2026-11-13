# cases/test_device_model.py
import pytest

from lib.device_model_api import list_device_models, add_device_model, del_device_model, get_device_id_list


def test_device_model_001_crud_full_flow(token, dev_cleaner):
    #新增
    add_resp = add_device_model(token, 3,'增删查全流程', '增删查全流程测试数据')
    add_data = add_resp.json()
    assert add_data['ret'] == 0
    new_id = add_data['id']
    dev_cleaner.append(new_id)
    # 校验新增是否成功
    id_list = get_device_id_list(token)
    assert new_id in id_list
    # 删除
    del_resp = del_device_model(token, new_id)
    del_data = del_resp.json()
    assert del_data['ret'] == 0
    # 校验删除是否成功
    id_list_after = get_device_id_list(token)
    assert new_id not in id_list_after

def test_add_device_model_002_add_normal(token, dev_cleaner):
    #新增
    add_resp = add_device_model(token, 3, '正常添加1234asdf', '正常添加测试数据')
    add_data = add_resp.json()
    new_id = add_data['id']
    dev_cleaner.append(new_id)
    assert add_data['ret'] == 0
    # 校验新增是否成功
    id_list = get_device_id_list(token)
    assert new_id in id_list

# 疑似bug:接口不会校验'数据类型'是否存在
@pytest.mark.xfail(reason='后端缺少typeid校验，错误数据当前可正常入库，待修复')
def test_add_device_model_003_invalid_typeid(token, dev_cleaner):
    add_resp = add_device_model(token, 100, '接口不校验', '接口不校验测试数据')   # 传入错误的typeid
    add_data = add_resp.json()
    if 'id' in add_data:
        new_id = add_data['id']
        dev_cleaner.append(new_id)

    assert add_data['ret'] != 0


def test_list_device_model_001_keywords_filter(token, dev_cleaner):
    add_resp = add_device_model(token, 1, '关键词过滤abcdddd', '关键词过滤测试数据')
    add_data = add_resp.json()
    new_id = add_data['id']
    dev_cleaner.append(new_id)

    # 存在关键词
    resp_match = list_device_models(token, keywords='abcdddd')
    data_match = resp_match.json()
    assert  data_match['ret'] == 0
    assert any(item['name'] == '关键词过滤abcdddd' for item in data_match['retlist'])

    # 不存在关键词
    resp_match2 = list_device_models(token, keywords='绝对不存在的词zzz')
    data_match2 = resp_match2.json()
    assert data_match2['ret'] == 0
    assert data_match2['retlist'] == []

def test_del_device_model_001_delete_existing(token, add_dev_data_test):
    new_id = add_dev_data_test  #新增一条临时数据并获取id，用例执行结束后会自动删除此条数据
    del_resp = del_device_model(token, new_id)
    del_data = del_resp.json()
    assert del_data['ret'] == 0

    id_list_after = get_device_id_list(token)
    assert new_id not in id_list_after

#  疑似bug:接口删除数据时不会校验'id'是否存在
@pytest.mark.xfail(reason='后端缺少删除不存在id校验，不存在数据当前可正常删除，待修复')
def test_del_device_model_002_delete_non_exist(token):
    del_resp = del_device_model(token, 10000)
    del_data = del_resp.json()
    assert del_data['ret'] != 0
