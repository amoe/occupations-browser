import ov_rest_server
import pytest
import json

def test_foo():
    client = ov_rest_server.app.test_client()
    result = client.get(
        path="/my-endpoint",
    )
    
    data = json.loads(result.get_data(as_text=True))
    assert data == {'foo': 42}

