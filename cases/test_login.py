# cases/test_login.py
from pathlib import Path

from lib.login_api import login
import pytest
import yaml


# 用 __file__ 定位 yaml，避免从不同目录启动 pytest 时找错文件
DATA_FILE = Path(__file__).parent / "data" / "login_cases.yaml"

def _load_login_fail_cases() -> list[dict]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f) or []

# 正常登陆成功
def test_login_001_normal_success():
    resp = login('byhy', 'sdfsdf')
    data = resp.json()
    assert data['ret'] == 0
    assert 'token' in data

# 登陆异常入参，预期失败
@pytest.mark.parametrize(
    'case',
    _load_login_fail_cases(),
    ids=lambda c: c['case_id'],
)
def test_login_002_param_failed_cases(case:dict):
    resp = login(case['username'], case['password'])
    data = resp.json()
    assert data['ret'] == case['expected_ret']
    assert data['msg'] == case['expected_msg']


