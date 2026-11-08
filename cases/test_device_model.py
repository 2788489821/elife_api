# cases/test_device_model.py

from lib.api_smp import list_device_models

def test_device_model(token):
    resp = list_device_models(token)
    data = resp.json()
    assert data["ret"] == 0

