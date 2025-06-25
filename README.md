# wtf-bot

A Flask application that powers the `/wtf` Slack command. Inspired by a [previous incarnation](https://github.com/paultag/wtf) of similar functionality. Relies on the VA [acronym list](https://github.com/department-of-veterans-affairs/acronyms).

## Install to slack

If using a VA slack instance, you can configure an instance of this bot into your slack.
To do this, follow these steps:

1. Create a new slack app in your workspace, using the [manifest](slack_app_config.yaml). Instructions to do this are [here](https://api.slack.com/reference/manifests#creating_apps).
1. Get the app approved by your administrators and add it to your workspace.
1. Submit a ticket to the [DOTS service desk](https://vajira.max.gov/servicedesk/customer/portal/1/create/17) and provide the 'Verification Token' available in the `Basic Information / App Config` section of your bot config.
   This token is used to validate your requests to the wtf-bot.
1. DOTS will inform you when the token has been added, and will provide you with the URL to the wtf-bot service. This
   URL should be added to your app config to replace the `http://replace.me.com/slack` link.
1. Test out the wtf-bot in your slack with `/wtf VA` - it should work!

## Local development

Clone this repo.

```
$ git clone https://github.com/department-of-veterans-affairs/wtf-bot.git
$ cd /path/to/wtf-bot/
```

### Set up python and poetry

1. Install python as defined in `.python-version`. You can use [Pyenv](https://github.com/pyenv/pyenv) or [asdf](https://asdf-vm.com/) to manage python versions. Verify with `python --version`
1. [Install poetry](https://python-poetry.org/docs/#installation)
1. Install the python dependencies:

```
make install
```

### Run tests

```
make test
```

## Run the server locally

### Set up environment variables

#### \*nix

```bash
export FLASK_APP=/path/to/wtf-bot/wtf_bot/wtf.py
export FLASK_DEBUG=1
export SLACK_TOKENS={comma separated tokens to be defined by you}
export DATA_URL=https://raw.githubusercontent.com/department-of-veterans-affairs/acronyms/master/acronyms.csv
```

#### Windows

```PowerShell
set FLASK_APP=/path/to/wtf-bot/wtf_bot/wtf.py
set FLASK_DEBUG=1
set SLACK_TOKENS={comma separated tokens to be defined by you}
set DATA_URL=https://raw.githubusercontent.com/department-of-veterans-affairs/acronyms/master/acronyms.csv
```

### Start the local server

```
poetry run flask run
```

## Query the `/slack` endpoint

```
curl -X POST http://127.0.0.1:5000/slack -d "text=aaa&token={to be defined by you}"
```

## Bugs, feature requests, or contributions

Open an [Issue](https://github.com/department-of-veterans-affairs/wtf-bot/issues). Pull requests welcome.
