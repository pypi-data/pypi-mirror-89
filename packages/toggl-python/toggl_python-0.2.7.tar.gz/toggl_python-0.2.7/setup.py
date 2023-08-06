# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toggl_python']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.16.1,<0.17.0', 'pydantic[email]>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'toggl-python',
    'version': '0.2.7',
    'description': 'Python wrapper for Toggl API.',
    'long_description': 'Toggl Python API\n================\n\n![https://pypi.python.org/pypi/toggl_python](https://img.shields.io/pypi/v/toggl_python.svg) ![https://travis-ci.com/evrone/toggl_python](https://img.shields.io/travis/evrone/toggl_python.svg) ![https://toggl-python.readthedocs.io/en/latest/?badge=latest](https://readthedocs.org/projects/toggl-python/badge/?version=latest) ![https://pyup.io/repos/github/evrone/toggl_python/](https://pyup.io/repos/github/evrone/toggl_python/shield.svg)\n\n\nToggl Python API\n----------------\n[<img src="https://evrone.com/logo/evrone-sponsored-logo.png" width=231>](https://evrone.com/?utm_source=github.com)  \n* Based on open Toggl API documentation: https://github.com/toggl/toggl_api_docs/blob/master/toggl_api.md\n* Free software: MIT license\n* Documentation: https://toggl-python.readthedocs.io.  \n\n\nInstallation\n------------\n`pip install toggl-python` or use [poetry](https://python-poetry.org) `poetry add toggl-python`\n\nFeatures\n--------\n\n- Get TimeEntries.\n\n```python\nfrom toggl_python import TokenAuth, TimeEntries\n\nif __name__ == "__main__":\n    auth = TokenAuth(\'AUTH_TOKEN\')\n    print(TimeEntries(auth=auth).list())\n```\n\n* *TODO*\n\nCredits\n-------\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.\n',
    'author': 'Ivlev Denis',
    'author_email': 'me@dierz.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/evrone/toggl_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
