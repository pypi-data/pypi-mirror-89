# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanicargs']

package_data = \
{'': ['*']}

install_requires = \
['ciso8601>=2.1.3,<3.0.0', 'sanic>=18.12']

setup_kwargs = {
    'name': 'sanicargs',
    'version': '2.1.0',
    'description': 'Parses query args or body parameters in sanic using type annotations',
    'long_description': '[![Build Status](https://travis-ci.org/trustpilot/python-sanicargs.svg?branch=master)](https://travis-ci.org/trustpilot/python-sanicargs) [![Latest Version](https://img.shields.io/pypi/v/sanicargs.svg)](https://pypi.python.org/pypi/sanicargs) [![Python Support](https://img.shields.io/pypi/pyversions/sanicargs.svg)](https://pypi.python.org/pypi/sanicargs)\n\n# Sanicargs\nParses query parameters and json body parameters for [Sanic](https://github.com/channelcat/sanic) using type annotations.\n\n## Survey\nPlease fill out [this survey](https://docs.google.com/forms/d/e/1FAIpQLSdNLvB7NEJQhUyVdaZpBAgS0f1k9OywZp8xDqhaNY0rl-unZA/viewform?usp=sf_link) if you are using Sanicargs, we are gathering feedback :-)\n\n## Install\nInstall with pip\n```\n$ pip install sanicargs\n```\n\n## Usage\n\nUse the `parse_parameters` decorator to parse query parameters (GET) or body parameters (POST) and type cast them together with path params in [Sanic](https://github.com/channelcat/sanic)\'s routes or blueprints like in this [example](https://github.com/trustpilot/python-sanicargs/tree/master/examples/simple.py) below:\n\n```python\nimport datetime\nfrom sanic import Sanic, response\nfrom sanicargs import parse_parameters\n\napp = Sanic("test_sanic_app")\n\n@app.route("/me/<id>/birthdate", methods=[\'GET\'])\n@parse_parameters\nasync def test_datetime(req, id: str, birthdate: datetime.datetime):\n    return response.json({\n        \'id\': id, \n        \'birthdate\': birthdate.isoformat()\n    })\n\nif __name__ == "__main__":\n  app.run(host="0.0.0.0", port=8080, access_log=False, debug=False)\n```\n\nTest it running with \n```bash\n$ curl \'http://0.0.0.0:8080/me/123/birthdate?birthdate=2017-10-30\'\n```\n\n### Query parameters\n\n* **str** : `ex: ?message=hello world`\n* **int** : `ex: ?age=100`\n* **bool** : `ex: ?missing=false`\n* **datetime.datetime** : `ex: ?currentdate=2017-10-30T10:10:30 or 2017-10-30`\n* **datetime.date** : `ex: ?birthdate=2017-10-30`\n* **List[str]** : `ex: ?words=you,me,them,we`\n\n### JSON body parameters\n\n{\n  "message": "hello word",\n  "age": 100,\n  "missing": false,\n  "currentDate": "2017-10-30",\n  "currentDateTime": "2017-10-30T10:10:30",\n  "words": ["you", "me", "them", "we"]\n}\n\n### Note about datetimes\n\nDates and datetimes are parsed without timezone information giving you a "naive datetime" object. See the note on [datetime.timestamp()](https://docs.python.org/3/library/datetime.html#datetime.datetime.timestamp) about handling timezones if you require epoch format timestamps.\n\n### Important notice about decorators\n\nThe sequence of decorators is, as usual, important in Python.\n\nYou need to apply the `parse_parameters` decorator as the first one executed which means closest to the `def`.\n\n### `request` is mandatory!\n\nYou should always have request as the first argument in your function in order to use `parse_parameters`.\n\n**Note** that `request` arg can be renamed and even type-annotated as long as it is the first arg.\n\n### `parse_query_args` deprecation\n\n`parse_query_args` will be deprecated in future version in favor of `parse_parameters`\nCurrently it is still usable as a legacy decorator\n',
    'author': 'Johannes Valbjørn',
    'author_email': 'jgv@trustpilot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trustpilot/python-sanicargs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
