import json
from core.libs import helpers

def test_ready(client):
    response = client.get('/')

    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['status'] == 'ready'


