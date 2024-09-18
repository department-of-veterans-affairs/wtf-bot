import os
import pytest
from config import Config


@pytest.fixture(autouse=True)
def preserve_env_vars():
    orig_data_url = os.getenv('DATA_URL')
    orig_slack_tokens = os.getenv('SLACK_TOKENS')
    yield
    os.environ['DATA_URL'] = orig_data_url
    os.environ['SLACK_TOKENS'] = orig_slack_tokens


@pytest.mark.parametrize("setting", ['DATA_URL', 'SLACK_TOKENS'])
def test_raises_exception_on_missing_setting(setting):
    del os.environ[setting]
    with pytest.raises(ValueError) as e:
        assert Config().__getattribute__(setting)
    assert str(e.value) == f'No {setting} environment variable set'


def test_handles_multiple_tokens_comma_separated():
    os.environ['SLACK_TOKENS'] = 'token1,token2,token3'
    assert Config().SLACK_TOKENS == ['token1', 'token2', 'token3']
