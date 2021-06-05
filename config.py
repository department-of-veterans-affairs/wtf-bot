from os import getenv


class Config(object):
    @property
    def SLACK_TOKENS(self):
        slack_tokens_string = getenv('SLACK_TOKENS')
        if not slack_tokens_string:
            raise ValueError("No SLACK_TOKENS environment variable set")
        return [token.strip() for token in slack_tokens_string.split(',')]

    @property
    def DATA_URL(self):
        data_url = getenv('DATA_URL')
        if not data_url:
            raise ValueError("No DATA_URL environment variable set")
        return data_url
