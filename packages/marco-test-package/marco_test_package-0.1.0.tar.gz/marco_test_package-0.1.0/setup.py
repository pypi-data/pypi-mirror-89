# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marco_test_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'marco-test-package',
    'version': '0.1.0',
    'description': 'Test package for marco',
    'long_description': '# Marco test package\n\n\n[![PyPI version](https://badge.fury.io/py/marco_test_package.svg)](https://badge.fury.io/py/marco_test_package)\n![versions](https://img.shields.io/pypi/pyversions/marco_test_package.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/marco_test_package.svg)](https://github.com/mgancita/marco_test_package/blob/main/LICENSE)\n\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\nTest package for marco\n\n\n- Free software: MIT\n- Documentation: https://mgancita.github.io/marco-test-package.\n\n\n## Features\n\n* TODO\n\n## Credits\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`mgancita/cookiecutter-pypackage`](https://mgancita.github.io/cookiecutter-pypackage/) project template.\n',
    'author': 'Marco Gancitano',
    'author_email': 'marco.gancitano@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mgancita/marco-test-package',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
