# cases/test_login.py

from lib.login_api import login
import pytest

# 正常登陆成功
def test_login_001_normal_success():
    resp = login('byhy', 'sdfsdf')
    data = resp.json()
    assert data['ret'] == 0
    assert 'token' in data

# 登陆异常入参，预期失败
@pytest.mark.parametrize('username, password, expected_ret, expected_msg',
    [
        (None, 'sdfsdf', 2,'用户名不存在'),   #疑似bug，此处msg应该返回'用户名不能为空'
        ('byhy', None, 3,'用户名或者密码错误'),  #疑似bug，此处msg应该返回'密码不能为空'
        ('byhy', 'sdfsdff', 3, '用户名或者密码错误'),
        ('byhy', 'sdfsd', 3, '用户名或者密码错误'),
        ('byhyy', 'sdfsdf', 2, '用户名不存在'),
        ('byh', 'sdfsdf', 2, '用户名不存在'),
    ]
)
def test_login_002_param_failed_cases(username, password, expected_ret, expected_msg):
    resp = login(username, password)
    data = resp.json()
    assert data['ret'] == expected_ret
    assert data['msg'] == expected_msg


