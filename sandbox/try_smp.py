# 探针脚本

from lib.device_model_api import list_device_models, add_device_model, del_device_model, get_device_id_list
from lib.login_api import login



resp = login('byhy', None)
print(resp.status_code)
data = resp.json()
print(data)
assert data['ret'] == 0
assert 'token' in data









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



