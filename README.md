# wtf-bot

A Flask application that powers the DSVA Slack /wtf command. Inspired by a [previous incarnation](https://github.com/paultag/wtf) of similiar functionality. Configured for deployment on [Cloud Foundry](https://www.cloudfoundry.org/). Relies on the VA [acronym list](https://github.com/department-of-veterans-affairs/acronyms).

## Local development

Clone this repo.
- `$ git clone https://github.com/department-of-veterans-affairs/wtf-bot.git`
- `$ cd /path/to/wtf-bot/`

Create and configure virtual environment.
- `$ python3 -m venv venv`
- `$ source venv/bin/activate`
- `$ pip3 install -r requirements.txt`

Set environment variables.
- `$ export FLASK_APP=/path/to/wtf-bot/wtf.py`
- `$ export FLASK_DEBUG=1`
- `$ export SLACK_TOKEN={to be defined by you}`
- `$ export DATA_URL=https://raw.githubusercontent.com/department-of-veterans-affairs/acronyms/master/acronyms.csv`

Run tests.
- `$ pytest tests_wtf.py`

Run the local server.
- `$ flask run`

Query the `/slack` endpoint.
- `$ curl -X POST http://127.0.0.1:5000/slack -d "text=aaa&token={to be defined by you}"`

## Bugs, feature requests, or contributions

Open an [Issue](https://github.com/department-of-veterans-affairs/wtf-bot/issues). Pull requests welcome.
