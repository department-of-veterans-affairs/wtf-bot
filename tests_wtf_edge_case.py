import http
import os
import json
import pytest
from wtf import APP

ROUTE = '/slack'
TEST_TOKENS = ['token1', 'token2']

@pytest.fixture
def client():
    client = APP.test_client()
    APP.config['TESTING'] = True
    APP.config['SLACK_TOKENS'] = TEST_TOKENS
    yield client

def test_env_vars_present():
    for var in ['SLACK_TOKENS', 'DATA_URL']:
        assert os.getenv(var) != None

@pytest.mark.parametrize("token", TEST_TOKENS)

def test_good_payload_using_valid_token(client, token):
    data = {'text': 'vba','token': token}
    r = client.post(ROUTE, data=data)
    assert b'Veterans Benefits Administration' in r.data
    assert r.status_code == http.HTTPStatus.OK

def test_multi_def_with_context_and_note_payload(client):
    data = {'text': 'foo','token': TEST_TOKENS[0]}
    r = client.post(ROUTE, data=data)
    # print (r.data)
    assert b'foo\n - For Obfuscating Obvious Information Def 1\n\t- This is a sample context\n\t- This is a sample note; \n - For Obfuscating Obvious Information Def 2\n\t- This is a sample context\n\t- This is a sample note; \n - For Obfuscating Obvious Information Def 3\n\t- This is a sample context\n\t- This is a sample note' in r.data

