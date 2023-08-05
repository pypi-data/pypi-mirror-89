# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lime_etl',
 'lime_etl.adapter',
 'lime_etl.domain',
 'lime_etl.service',
 'lime_etl.service.admin']

package_data = \
{'': ['*'], 'lime_etl.domain': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['lime-uow>=0.1.43,<0.2.0', 'sqlalchemy>=1.3.19,<2.0.0']

setup_kwargs = {
    'name': 'lime-etl',
    'version': '0.1.27',
    'description': 'Simple ETL job runner',
    'long_description': None,
    'author': 'Mark Stefanovic',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
