# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_hypothesis']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'hypothesis-auto>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-hypothesis',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>fastapi-hypothesis</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/fastapi-hypothesis" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/fastapi-hypothesis" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/fastapi-hypothesis/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/fastapi-hypothesis">\n    <br />\n    <a href="https://pypi.org/project/fastapi-hypothesis" target="_blank">\n        <img src="https://img.shields.io/pypi/v/fastapi-hypothesis" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/fastapi-hypothesis">\n    <img src="https://img.shields.io/github/license/Kludex/fastapi-hypothesis">\n</p>\n\n\n## Installation\n\n``` bash\npip install fastapi-hypothesis\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/fastapi-hypothesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
