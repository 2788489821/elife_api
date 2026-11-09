# cases/test_device_model.py

from lib.api_smp import list_device_models, add_device_model, del_device_model


def test_device_model(token):

    add_resp = add_device_model(token, 3,'0004', 'ms3')
    add_data = add_resp.json()
    assert add_data["ret"] == 0
    new_id = add_data["id"]

    list_resp = list_device_models(token)
    assert list_resp.json()["ret"] == 0

    del_resp = del_device_model(token, new_id)
    del_data = del_resp.json()
    assert del_data["ret"] == 0

    list_resp2 = list_device_models(token)
    list_data2 = list_resp2.json()
    assert list_resp2.json()["ret"] == 0
    id_list = [item["id"] for item in list_data2["retlist"]]
    assert new_id not in id_list

