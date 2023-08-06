# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplecrud']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.2,<0.62.0', 'pydantic>=1.7.2,<2.0.0']

extras_require = \
{'sqlalchemy': ['SQLAlchemy>=1.3.20,<2.0.0']}

entry_points = \
{'console_scripts': ['check_format = scripts:check_format',
                     'format = scripts:format',
                     'lint = scripts:lint',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'simplecrud',
    'version': '1.0.0',
    'description': 'Simple CRUD for FastAPI applications.',
    'long_description': '<p align="center">\n    <em>Simple CRUD - Created by and for FastAPI users</em>\n</p>\n<p align="center">\n<img src="https://img.shields.io/github/last-commit/Kludex/simplecrud.svg">\n<a href="https://codecov.io/gh/Kludex/simplecrud" target="_blank">\n    <img src="https://codecov.io/gh/Kludex/simplecrud/branch/main/graph/badge.svg?token=J6D4HJ4G9X" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/simplecrud" target="_blank">\n    <img src="https://badge.fury.io/py/simplecrud.svg" alt="Package version">\n</a>\n    <img src="https://img.shields.io/pypi/pyversions/simplecrud.svg">\n    <img src="https://img.shields.io/github/license/Kludex/simplecrud.svg">\n</p>\n\n---\n\nPackage based on the FastAPI [cookiecutter](https://github.com/cookiecutter/cookiecutter) [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/crud/base.py)\n\n---\n\n## Installation\n\n```bash\npip install simplecrud\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/simplecrud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
