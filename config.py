from os import getenv

SLACK_TOKENS = [token.strip() for token in getenv('SLACK_TOKENS').split(',')]
DATA_URL = getenv('DATA_URL')
