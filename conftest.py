# conftest.py

import pytest
from lib.api_smp import login

@pytest.fixture(scope='module')
def token():
    resp = login('byhy','sdfsdf')
    data = resp.json()
    assert data['ret'] == 0

    yield data['token']
