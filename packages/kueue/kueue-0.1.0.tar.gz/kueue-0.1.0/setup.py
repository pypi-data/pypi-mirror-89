# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kueue']

package_data = \
{'': ['*']}

install_requires = \
['confluent-kafka>=1.5.0,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'kueue',
    'version': '0.1.0',
    'description': 'Distributed Task Queue - using Kubernetes and Kafka',
    'long_description': None,
    'author': 'Jose Rojas',
    'author_email': 'jose.rojas95@mail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
