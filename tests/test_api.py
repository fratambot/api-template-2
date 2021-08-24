import json

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.main import app


# Testing pytest
def test_always_passes():
    assert True


@pytest.mark.xfail()
def test_always_fails():
    assert False


# Testing api responses
client = TestClient(app)


def test_status(disable_network_calls):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Ok"}


def test_get_array(disable_network_calls):
    response = client.get("/array")
    parsed_response = json.loads(response.text)
    print(parsed_response) # test and fix not authenticated
    array_restored = np.array(parsed_response["result"])
    assert isinstance(array_restored, np.ndarray)
    assert array_restored.shape == (5,)
