# cases/test_login.py

from lib.api_smp import login

def test_login():
    resp = login('byhy', 'sdfsdf')
    print(resp.status_code)
    data = resp.json()
    print(data)
    assert data['ret'] == 0
    assert 'token' in data

