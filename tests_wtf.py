import os

# Update/add env variables for this subprocess to test multiple Slack tokens.
# Must be done before wtf.APP and config.SLACK_TOKENS are imported.
os.environ['SLACK_TOKENS'] = 'test_token0, test_token1, test_token2'

import json
import pytest
from config import SLACK_TOKENS
from wtf import APP

TEST_TOKEN = SLACK_TOKENS[2]
ROUTE = '/slack'

@pytest.fixture
def client():
    client = APP.test_client()
    APP.config['TESTING'] = True
    yield client

def test_env_vars_present():
    for var in ['SLACK_TOKENS', 'DATA_URL']:
        assert os.getenv(var) != None

def test_different_slack_token(client):
    data = {'text': 'vba','token': SLACK_TOKENS[1]}
    r = client.post(ROUTE, data=data)
    assert r.status_code != 401

def test_good_payload(client):
    data = {'text': 'vba','token': TEST_TOKEN}
    r = client.post(ROUTE, data=data)
    assert b'Veterans Benefits Administration' in r.data

def test_multi_def_payload(client):
    data = {'text': 'aaa','token': TEST_TOKEN}
    r = client.post(ROUTE, data=data)
    assert b'Abdominal Aortic Aneurysm; or Area Agencies on Aging;' in r.data

def test_comma_in_def(client):
    data = {'text': 'acre','token': TEST_TOKEN}
    r = client.post(ROUTE, data=data)
    assert b'A measure of land 43,560 sq. ft.' in r.data

def test_bad_payload(client):
    data = {'foo': 'bar', 'token': TEST_TOKEN}
    r = client.post(ROUTE, data=data)
    assert b'Improper request' in r.data

def test_no_slack_token(client):
    data = {'text': 'vba','token': ' foobar'}
    r = client.post(ROUTE, data=data)
    assert b'Not authorized' in r.data

def test_not_found(client):
    data = {'text': '13231312334','token': TEST_TOKEN}
    r = client.post(ROUTE, data=data)
    assert b'not found!' in r.data
    assert b'13231312334' in r.data
