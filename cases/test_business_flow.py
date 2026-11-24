# cases/test_business_flow.py
from lib.device_model_api import add_device_model, get_device_id_list, del_device_model
from lib.service_rule_api import build_charge_rule_by_type, add_service_rule, get_service_rule_id, del_service_rule


def test_business_flow(token, dev_cleaner, ser_cleaner):
    # 新增设备类型数据
    add_resp = add_device_model(token, 3, '增删查全流程', '增删查全流程测试数据')
    add_data = add_resp.json()
    assert add_data['ret'] == 0, f"设备类型新增失败，接口返回：{add_data}"
    new_dev_id = add_data['id']
    dev_cleaner.append(new_dev_id)
    # 校验新增是否成功
    id_list = get_device_id_list(token)
    assert new_dev_id in id_list, f"新增后列表中未查到设备类型 id={new_dev_id}，当前列表：{id_list}"

    # 构造报文
    charge_rule = build_charge_rule_by_type("prepaid_volume", (55, 66, "", "磅", "0.23"))
    # 新增业务规则数据
    add_resp = add_service_rule(token, "重量单", 1, charge_rule, "重量计费规则")
    add_data = add_resp.json()
    assert add_data["ret"] == 0, f"业务规则新增失败，接口返回：{add_data}"
    new_ser_id = add_data["id"]
    ser_cleaner.append(new_ser_id)
    # 校验新增是否成功
    id_list = get_service_rule_id(token)
    assert new_ser_id in id_list, f"新增后列表中未查到业务规则 id={new_ser_id}，当前列表：{id_list}"

    # 删除业务规则数据
    resp = del_service_rule(token, new_ser_id)
    del_data = resp.json()
    assert del_data["ret"] == 0, f"业务规则删除失败，接口返回：{del_data}"

    # 校验删除是否成功
    id_list_after = get_service_rule_id(token)
    assert new_ser_id not in id_list_after, f"业务规则删除后仍存在 id={new_ser_id}，当前列表：{id_list_after}"

    # 删除设备类型数据
    del_resp = del_device_model(token, new_dev_id)
    del_data = del_resp.json()
    assert del_data['ret'] == 0, f"设备类型删除失败，接口返回：{del_data}"
    # 校验删除是否成功
    id_list_after = get_device_id_list(token)
    assert new_dev_id not in id_list_after, f"设备类型删除后仍存在 id={new_ser_id}，当前列表：{id_list_after}"