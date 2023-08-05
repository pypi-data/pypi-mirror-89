# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyergast']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.5,<2.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'pyergast',
    'version': '0.1.0',
    'description': 'Python pandas wrapper for the Ergast F1 API',
    'long_description': '# pyErgast \n\n![](https://github.com/weiranyu/pyergast/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/weiranyu/pyergast/branch/main/graph/badge.svg)](https://codecov.io/gh/weiranyu/pyergast) ![Release](https://github.com/weiranyu/pyergast/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/pyergast/badge/?version=latest)](https://pyergast.readthedocs.io/en/latest/?badge=latest)\n\nPython pandas wrapper for the Ergast F1 API\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ pyergast\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://pyergast.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/weiranyu/pyergast/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Weiran Yu',
    'author_email': 'weiranyu@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/weiranyu/pyErgast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
