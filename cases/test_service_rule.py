import allure
import pytest

from lib.service_rule_api import (
    add_service_rule,
    get_service_rule_id,
    del_service_rule,
    list_service_rule,
    build_charge_rule_by_type,
)


# ============ 测试数据（与代码分离） ============
CRUD_CASES = [
    {
        "title": "运费单-预付费下发业务量",
        "name": "运费单",
        "rule_type_id": 1,
        "args": (2, 50, "", "元/km", "1.3"),
        "desc": "运费计费规则",
        "type_name": "prepaid_volume",
        "severity": allure.severity_level.CRITICAL,
    },
    {
        "title": "打包费单-预付费下发费用",
        "name": "打包费单",
        "rule_type_id": 2,
        "args": (1, 7),
        "desc": "打包费计费规则",
        "type_name": "prepaid_fee",
        "severity": allure.severity_level.CRITICAL,
    },
    {
        "title": "点餐订单-后付费上报业务量",
        "name": "点餐订单",
        "rule_type_id": 3,
        "args": ([(1, "元/份", 20.4), (24, "元/串", 8), (7, "元/瓶", 3)],),
        "desc": "点餐订单计费规则",
        "type_name": "postpaid",
        "severity": allure.severity_level.CRITICAL,
    },
]


@allure.feature("业务规则管理")
@allure.tag("每周执行一次")
class TestServiceRule:

    @allure.story("增删查全流程")
    @pytest.mark.parametrize("case", CRUD_CASES, ids=lambda c: c["title"])
    def test_001_full_flow(self, token, ser_cleaner, case):
        allure.dynamic.title(case["title"])
        allure.dynamic.severity(case["severity"])

        with allure.step("根据类型构造 charge_rule 报文"):
            charge_rule = build_charge_rule_by_type(case["type_name"], case["args"])

        with allure.step("调用新增业务规则接口"):
            add_resp = add_service_rule(token, case["name"], case["rule_type_id"], charge_rule, case["desc"])
            add_data = add_resp.json()
            assert add_data["ret"] == 0, f"新增失败，接口返回：{add_data}"
            new_id = add_data["id"]
            ser_cleaner.append(new_id)

        with allure.step("查询列表，校验新增成功"):
            id_list = get_service_rule_id(token)
            assert new_id in id_list, f"新增后列表中未查到 id={new_id}，当前列表：{id_list}"

        with allure.step("调用删除业务规则接口"):
            resp = del_service_rule(token, new_id)
            del_data = resp.json()
            assert del_data["ret"] == 0, f"删除失败，接口返回：{del_data}"

        with allure.step("再次查询列表，校验删除成功"):
            id_list_after = get_service_rule_id(token)
            assert new_id not in id_list_after, f"删除后仍存在 id={new_id}，当前列表：{id_list_after}"

    @allure.story("新增业务规则")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("新增合法业务规则")
    def test_002_add_normal(self, token, ser_cleaner):
        with allure.step("构造预付费下发业务量报文"):
            charge_rule = build_charge_rule_by_type("prepaid_volume", (55, 66, "", "磅", "0.23"))

        with allure.step("调用新增业务规则接口"):
            add_resp = add_service_rule(token, "重量单", 1, charge_rule, "重量计费规则")
            add_data = add_resp.json()
            assert add_data["ret"] == 0, f"新增失败，接口返回：{add_data}"
            new_id = add_data["id"]
            ser_cleaner.append(new_id)

        with allure.step("查询列表，校验新增成功"):
            id_list = get_service_rule_id(token)
            assert new_id in id_list, f"新增后列表中未查到 id={new_id}，当前列表：{id_list}"

    @allure.story("新增业务规则")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("新增非法 type_id，预期后端拦截（已知缺陷 xfail）")
    @pytest.mark.xfail(reason="后端缺少 type_id 校验，错误数据当前可正常入库，待修复")
    def test_003_add_invalid_typeid(self, token, ser_cleaner):
        with allure.step("构造预付费下发业务量报文"):
            charge_rule = build_charge_rule_by_type("prepaid_volume", (55, 66, "", "磅", "0.23"))

        with allure.step("使用非法 rule_type_id=4 调用新增接口"):
            add_resp = add_service_rule(token, "重量单", 4, charge_rule, "重量计费规则")
            add_data = add_resp.json()
            if "id" in add_data:
                ser_cleaner.append(add_data["id"])

        with allure.step("断言后端拦截非法类型"):
            assert add_data["ret"] != 0, f"非法 type_id 应被拦截，实际入库成功，返回：{add_data}"

    @allure.story("查询业务规则")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("业务规则关键词过滤")
    def test_004_keywords_filter(self, token, ser_cleaner):
        name = "关键词过滤abcdddd@#$%^"

        with allure.step("构造报文，新增带关键词的业务规则"):
            charge_rule = build_charge_rule_by_type("prepaid_volume", (55, 66, "", "磅", "0.23"))
            add_resp = add_service_rule(token, name, 1, charge_rule, "重量计费规则")
            add_data = add_resp.json()
            assert add_data["ret"] == 0, f"前置新增失败，接口返回：{add_data}"
            new_id = add_data["id"]
            ser_cleaner.append(new_id)

        with allure.step("使用存在的关键词查询，校验匹配"):
            resp_match = list_service_rule(token, keywords="abcdddd")
            data_match = resp_match.json()
            assert data_match["ret"] == 0, f"查询失败，接口返回：{data_match}"
            assert any(item["name"] == name for item in data_match["retlist"]), \
                f"关键词 abcdddd 未匹配到 {name}，返回列表：{data_match['retlist']}"

        with allure.step("使用不存在的关键词查询，校验返回空列表"):
            resp_match2 = list_service_rule(token, keywords="绝对不存在的词zzz")
            data_match2 = resp_match2.json()
            assert data_match2["ret"] == 0, f"查询失败，接口返回：{data_match2}"
            assert data_match2["retlist"] == [], f"不存在关键词应返回空列表，实际：{data_match2['retlist']}"

    @allure.story("删除业务规则")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("删除存在的业务规则")
    def test_005_delete_existing(self, token, ser_cleaner, add_ser_data_test):
        new_id = add_ser_data_test

        with allure.step("调用删除接口删除已存在规则"):
            resp = del_service_rule(token, new_id)
            del_data = resp.json()
            assert del_data["ret"] == 0, f"删除失败，接口返回：{del_data}"

        with allure.step("查询列表，校验已经删除"):
            id_list_after = get_service_rule_id(token)
            assert new_id not in id_list_after, f"删除后仍存在 id={new_id}，当前列表：{id_list_after}"

    @allure.story("删除业务规则")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("删除不存在 id，预期后端拦截（已知缺陷 xfail）")
    @pytest.mark.xfail(reason="后端缺少删除不存在 id 校验，不存在数据当前可正常删除，待修复")
    def test_006_delete_non_exist(self, token):
        with allure.step("调用删除接口，传入不存在 id"):
            resp = del_service_rule(token, 1234567)
            del_data = resp.json()

        with allure.step("断言后端拦截无效删除"):
            assert del_data["ret"] != 0, f"删除不存在 id 应被拦截，实际返回：{del_data}"
