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
    'version': '0.1.2',
    'description': 'Distributed Task Queue - backed by Kafka',
    'long_description': '## Kueue\n![Build](https://github.com/jarojasm95/kueue/workflows/Build/badge.svg)\n\nPython Distributed Task Queue - backed by Kafka\n\n\n## Motivation\nKueue was born out of the lack of a library that leverages [Kafka](https://kafka.apache.org/) for distributed task processing\n\n## Features\n- simple\n- intuitive api\n- extensible\n\n## Code Example\n```python\nimport time\nfrom kueue import task, TaskExecutorConsumer, KueueConfig\n\nKueueConfig(\n    kafka_bootstrap=\'localhost:9092\'\n)\n\n@task(topic="my-topic")\ndef sleepy_task(sleep: int):\n    time.sleep(sleep)\n    print("done sleeping", sleep)\n    return sleep\n\nsleepy_task.enqueue(args=(15,))\n\nconsumer = TaskExecutorConsumer(["my-topic"])\nconsumer.start()\n# prints "done sleeping, 15"\n```\n\n## Installation\n```\npip install kueue\n```\n\n## Development\n\nInstall [poetry](https://python-poetry.org/) and run `poetry install` at the root of the repository. This should create a virtual environment with all the necessary python dependencies.\n\n## Tests\nThe test framework makes heavy use of `pytest` fixtures in order to spin up full integration environment consisting of a kubernetes cluster using [kind](https://kind.sigs.k8s.io/) and [pytest-kind](https://codeberg.org/hjacobs/pytest-kind) and kafka using [strimzi](https://strimzi.io/)\n\n`pytest`\n\n## License\n\nMIT © [Jose Rojas](https://github.com/jarojasm95)\n',
    'author': 'Jose Rojas',
    'author_email': 'jose.rojas95@mail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jarojasm95/kueue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
