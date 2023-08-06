# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiyu_sso', 'qiyu_sso.forms', 'qiyu_sso.resp']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2']

setup_kwargs = {
    'name': 'qiyu-sso',
    'version': '0.1.0',
    'description': 'SSO client from QiYuTech',
    'long_description': '# qiyu-sso\nSSO Client from QiYuTech\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
