import csv
import http
import requests
from flask import Flask, make_response, request
from config import Config

APP = Flask(__name__)
APP.config.from_object(Config())

# flake8: noqa: C901
@APP.route('/slack', methods=['GET', 'POST'])
def slack():

    req = dict(request.form)

    if not all(k in req.keys() for k in ['text', 'token']):
        return make_response('Improper request.', http.HTTPStatus.BAD_REQUEST)

    if req['token'] not in APP.config['SLACK_TOKENS']:
        return make_response('Not authorized', 401)

    raw = requests.get(APP.config['DATA_URL'])

    decoded = raw.content.decode('utf-8')

    reader = csv.reader(decoded.split('\n'), delimiter=',')

    data = [r for r in reader if len(r) > 1]

    term_dict = {}

    for d in data:
        if len(d) != 4:
            continue
        acroynm = d[0].lower()
        definition = d[1].strip()
        context = ''
        notes = ''
        if len(d[2]) > 0:
            context = "\n\t- " + d[2].strip()
        if len(d[3]) > 0:
            notes = "\n\t- " + d[3].strip()
        full_data = "{}{}{}".format(definition, context, notes)

        existing = term_dict.get(acroynm, None)

        if not existing:
            term_dict[acroynm] = [full_data]

        else:
            term_dict[acroynm] = existing + [full_data]

    try:

        acroynm_defined = term_dict[req['text'].lower()]

        if len(acroynm_defined) > 1:
            response = ' - ' + '; \n - '.join(acroynm_defined)

        else:
            response = ' - ' + acroynm_defined[0]

        response = req['text'] + '\n' + response

    except KeyError:
        response = """
        Entry for '{}' not found! Acronyms may be added at
        https://github.com/department-of-veterans-affairs/acronyms
        """.format(req['text'])

    return make_response(response)
