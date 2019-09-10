import os, json
import pytest
from wtf import APP

ROUTE = '/slack'

@pytest.fixture
def client():
    client = APP.test_client()
    APP.config['TESTING'] = True
    yield client

def test_env_vars_present():
    for var in ['SLACK_TOKEN', 'DATA_URL']:
        assert os.getenv(var) != None

def test_good_payload(client):
    data = {'text': 'vba','token': os.getenv('SLACK_TOKEN')}
    r = client.post(ROUTE, data=data)
    assert b'Veterans Benefits Administration' in r.data

def test_multi_def_payload(client):
    data = {'text': 'aaa','token': os.getenv('SLACK_TOKEN')}
    r = client.post(ROUTE, data=data)
    assert b'Abdominal Aortic Aneurysm; or Area Agencies on Aging;' in r.data

def test_comma_in_def(client):
    data = {'text': 'acre','token': os.getenv('SLACK_TOKEN')}
    r = client.post(ROUTE, data=data)
    assert b'A measure of land 43,560 sq. ft.' in r.data

def test_bad_payload(client):
    data = {'foo': 'bar', 'token': os.getenv('SLACK_TOKEN')}
    r = client.post(ROUTE, data=data)
    assert b'Improper request' in r.data

def test_no_slack_token(client):
    data = {'text': 'vba','token': '13231312334'}
    r = client.post(ROUTE, data=data)
    assert b'Not authorized' in r.data

def test_not_found(client):
    data = {'text': '13231312334','token': os.getenv('SLACK_TOKEN')}
    r = client.post(ROUTE, data=data)
    assert b'not found!' in r.data
    assert b'13231312334' in r.data
