import io
import os
import tempfile
from backend import service
import numpy as np

import pytest


@pytest.fixture
def app():
    app_ = service.create_app()
    return app_


@pytest.fixture
def client(app):
    return app.test_client()


def test_api_get(client):
    file = 'logo.png'
    response = client.get('/api/get/' + file)
    data = np.fromstring(response.data, dtype=np.uint8)
    assert response.status_code == 200
    assert data.shape[0] == 6849
