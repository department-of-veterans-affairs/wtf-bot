import os
import csv
import requests
from flask import Flask, make_response, request
from config import SLACK_TOKEN, DATA_URL

APP = Flask(__name__)

@APP.route('/slack', methods=['GET', 'POST'])
def slack():

    req = dict(request.form)

    if not all(k in req.keys() for k in ['text', 'token']):
        return make_response('Improper request.', 400)

    if not req['token'] == SLACK_TOKEN:
        return make_response('Not authorized', 401)

    raw = requests.get(DATA_URL)

    decoded = raw.content.decode('utf-8')

    reader = csv.reader(decoded.split('\n'), delimiter=',')

    data = [r for r in reader if len(r) > 1]

    term_dict = {}

    for d in data:

        acroynm = d[0].lower()

        existing = term_dict.get(acroynm, None)

        if not existing:
            term_dict[acroynm] = [d[1]]

        else:
            term_dict[acroynm] = existing + [d[1]]

    try:

        acroynm_defined = term_dict[req['text'].lower()]

        if len(acroynm_defined) > 1:
            response = '; or '.join(acroynm_defined)

        else:
            response = acroynm_defined[0]

    except KeyError:
        response = """
        Not found! Acronyms may be added at
        https://github.com/department-of-veterans-affairs/acronyms
        """

    return make_response(response)
