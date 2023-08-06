# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['karmabot', 'karmabot.commands', 'karmabot.db']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.17,<2.0.0',
 'feedparser==5.2.1',
 'humanize>=2.4.0,<3.0.0',
 'importlib-metadata>=1.6.1,<2.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pyjokes>=0.6.0,<0.7.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'slackclient==1.3.1']

entry_points = \
{'console_scripts': ['karmabot = karmabot.main:main']}

setup_kwargs = {
    'name': 'karmabot',
    'version': '1.3',
    'description': 'A bot for Slack',
    'long_description': '# PyBites Karmabot - A Python based Slack Chatbot\n\n[![Tests](https://github.com/PyBites-Open-Source/karmabot/workflows/Tests/badge.svg)](https://github.com/PyBites-Open-Source/karmabot/actions?workflow=Tests) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![codecov.io](https://codecov.io/github/PyBites-Open-Source/karmabot/coverage.svg?branch=master)](https://codecov.io/github/PyBites-Open-Source/karmabot?branch=master)\n\n**A Python based Slack Chatbot for Community interaction**\n\n## Features\n\nKarmabot\'s main features is the management of Karma within the slack community server. You can give karma, reduce karma, check your current karma points and manage your karma related username.\n\n![karma example](https://www.pogross.de/uploads/karmabot.png)\n\nhttps://www.youtube.com/watch?v=Yx9qYl6lmzM&amp;t=2s\n\nAdditional commands / features are:\n\n- Jokes powered by [PyJokes](https://github.com/pyjokes/pyjokes)\n- Overview on top channels of the slack server\n- Random Python tip, quote or nugget from CodeChalleng.es\n- Browse and search python documentation, "pydoc help"\n\n## Installation\n\n`pip install karmabot`\n\n## Basic Usage\n\nAfter installing you can start karmabot by using the command\n\n```bash\nkarmabot\n```\n\nHowever, you need to supply some settings prior to this.\n\n### Settings\n\nBy default we will look for a `.karmabot` file in the directory you used the `karmabot` command. The file should supply the following information.\n\n```env\nKARMABOT_SLACK_USER=\nKARMABOT_SLACK_TOKEN=\nKARMABOT_SLACK_INVITE_USER_TOKEN=\nKARMABOT_DATABASE_URL=\nKARMABOT_GENERAL_CHANNEL=\nKARMABOT_ADMINS=\n```\n\n- KARMABOT_SLACK_USER\n  The [bot\'s slack user id](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace). Once you\'ve created your own Karmabot app, you can view its configuration details from the [My Apps](https://api.slack.com/apps/) page. The user ID shows up under **Basic Information --> App Credentials --> App ID**.\n\n- KARMABOT_SLACK_TOKEN\n  The [auth token](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace) for your bot. You can find the token from the [My Apps](https://api.slack.com/apps/) page for your Karmabot under **OAuth & Permissions --> Tokens for Your Workspace --> Bot User OAuth Access Token**. It starts with `xoxb-`.\n\n- KARMABOT_SLACK_INVITE_USER_TOKEN\n  An invite token to invite the bot to new channels. Bots cannot autojoin channels, but we implemented an invite procedure for this.\n\n- KARMABOT_DATABASE_URL\n  The database url which should be compatible with SqlAlchemy. For the provided docker file use postgres://user42:pw42@localhost:5432/karmabot.\n\n  - **Note:** To start the provided Docker-based Postgres server, be sure you have Docker Compose [installed](https://docs.docker.com/compose/install/) and run `docker-compose up` from the karmabot directory.\n\n- KARMABOT_GENERAL_CHANNEL\n  The channel id of your main channel slack\n\n- KARMABOT_ADMINS\n  The [slack user ids](https://api.slack.com/methods/users.identity) of the users that should have admin command access separated by commas.\n\nIf you do not want to use a file you have to provide environment variables with the above names. If no file is present we default to environment variables.\n\n## Development pattern for contributors\n\nWe use [poetry](https://github.com/python-poetry/poetry) and `pyproject.toml` for managing packages, dependencies and some settings.\n\n### Setup virtual environment for development\n\nYou should follow the [instructions](https://github.com/python-poetry/poetry) to get poetry up and running for your system. We recommend to use a UNIX-based development system (Linux, Mac, WSL). After setting up poetry you can use `poetry install` within the project folder to install all dependencies.\n\nThe poetry virtual environment should be available in the the project folder as `.venv` folder as specified in `poetry.toml`. This helps with `.venv` detection in IDEs.\n\n#### Conda users\n\nIf you use the Anaconda Python distribution (strongly recommended for Windows users) and `conda create` for your virtual environments, then you will not be able to use the `.venv` environment created by poetry because it is not a conda environment. If you want to use `poetry` disable poetry\'s behavior of creating a new virtual environment with the following command: `poetry config virtualenvs.create false`. You can add `--local` if you don\'t want to change this setting globally but only for the current project. See the [poetry configuration docs](https://python-poetry.org/docs/configuration/) for more details.\n\nNow, when you run `poetry install`, poetry will install all dependencies to your conda environment. You can verify this by running `pip freeze` after `poetry install`.\n\n### Testing and linting\n\nFor testing you need to install [nox](https://nox.thea.codes/en/stable/) separately from the project venv created by poetry. For testing just use the `nox` command within the project folder. You can run all the nox sessions separately if need, e.g.,\n\n- only linting `nox -rs lint`\n- only testing `nox -rs tests`\n\nIf `nox` cannot be found, use `python -m nox` instead.\n\nFor different sessions see the `nox.py` file. You can run `nox --list` to see a list of all available sessions.\n\nPlease make sure all tests and checks pass before opening pull requests!\n\n#### Using nox under Windows and Linux (WSL)\n\nMake sure to delete the `.nox` folder when you switch from Windows to WSL and vice versa, because the environments are not compatible.\n\n### [pre-commit](https://pre-commit.com/)\n\nTo ensure consistency you can use pre-commit. `pip install pre-commit` and after cloning the karmabot repo run `pre-commit install` within the project folder.\n\nThis will enable pre-commit hooks for checking before every commit.\n',
    'author': 'PyBites',
    'author_email': 'info@pybit.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PyBites-Open-Source/karmabot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
