# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verval']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'dacite>=1.6.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'verval',
    'version': '0.1.0',
    'description': 'Client python verval* sdm.data.kemdikbud',
    'long_description': '# verval\nClient python verval* sdm.data.kemdikbud\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dapodix/verval',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
