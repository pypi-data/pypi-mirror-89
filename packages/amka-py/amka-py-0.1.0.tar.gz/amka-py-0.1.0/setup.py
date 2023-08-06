# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amka_py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'amka-py',
    'version': '0.1.0',
    'description': 'A validator for greek social security number (AMKA)',
    'long_description': '# amka-py\n\n<a href="https://pypi.python.org/pypi/amka-py"><img alt="Pypi version" src="https://img.shields.io/pypi/v/amka-py.svg"></a>\n![CI](https://github.com/zoispag/amka-py/workflows/CI/badge.svg)\n\nA validator for greek social security number (AMKA)\n\n## Installation\n\n```bash\npip install amka-py\n```\n## Usage\n\n```python\nfrom amka_py.amka import validate\n\n# An invalid AMKA\nis_valid, err = validate("09095986680")\nprint(is_valid) # False\nprint(err)\n\n# A valid AMKA\nis_valid, err = validate("09095986684");\nprint(is_valid) # True\n```\n',
    'author': 'Zois Pagoulatos',
    'author_email': 'zpagoulatos@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zoispag/amka-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
