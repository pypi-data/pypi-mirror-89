# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_fastapi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytest-fastapi',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>pytest-fastapi</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/pytest-fastapi" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/pytest-fastapi" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/pytest-fastapi/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/pytest-fastapi">\n    <br />\n    <a href="https://pypi.org/project/pytest-fastapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/pytest-fastapi" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/pytest-fastapi">\n    <img src="https://img.shields.io/github/license/Kludex/pytest-fastapi">\n</p>\n\n\n## Installation\n\n``` bash\npip install pytest-fastapi\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/pytest-fastapi',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
