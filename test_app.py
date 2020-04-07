import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client
    


def test_send_message(client):
    """Start with a blank database."""

    rv = client.get('/send_message')
    assert b'OK GET' in rv.data



def test_post_messages(client):
    """Test that messages work."""

    rv = client.post('/send_message', data=dict({'name': 'serg', 'email':'serg@gmail,com', 'message': 'HI!' }))
    assert  b'OK POST' in rv.data

       