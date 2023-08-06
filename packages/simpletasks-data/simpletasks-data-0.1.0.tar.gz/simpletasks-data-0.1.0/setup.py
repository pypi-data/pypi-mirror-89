# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletasks_data']

package_data = \
{'': ['*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.4,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'simpletasks>=0.1.0,<0.2.0']

extras_require = \
{'geoalchemy': ['GeoAlchemy2>=0.8.4,<0.9.0']}

setup_kwargs = {
    'name': 'simpletasks-data',
    'version': '0.1.0',
    'description': 'A simple library to import data into a database from different sources (extensible)',
    'long_description': '# simpletasks-data\n\nSimple tasks runner for Python\n\n\n----\nContributing\n\n```\npoetry install --no-root\npoetry install -E geoalchemy\n```',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/simpletasks-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
