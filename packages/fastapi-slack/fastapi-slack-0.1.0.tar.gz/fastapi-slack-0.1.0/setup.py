# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fastapi_slack']
setup_kwargs = {
    'name': 'fastapi-slack',
    'version': '0.1.0',
    'description': 'Slack extension for FastAPI.',
    'long_description': '# fastapi-slack\n\nSlack extension for FastAPI.\n\n## Configuration - Environment Variables\n\n### `slack_access_token`\n\nBot User OAuth Access Token as defined in OAuth & Permissions menu of the slack app.\n\n### `slack_signing_secret`\n\nApp signing secret as shown in Basic Information menu of the slack app in the App\nCredentials section.\n\n\n## Setup\n\n* Include fastapi-slack router:\n\n```python\nimport fastapi_slack\nfrom fastapi import FastAPI\n\n\napp = FastAPI()\n\napp.include_router(fastapi_slack.router)\n```\n',
    'author': 'Hadrien David',
    'author_email': 'hadrien@dialogue.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dialoguemd/fastapi-slack',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
