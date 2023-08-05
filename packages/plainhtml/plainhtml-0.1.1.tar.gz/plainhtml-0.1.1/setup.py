# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plainhtml']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.2,<5.0.0']

setup_kwargs = {
    'name': 'plainhtml',
    'version': '0.1.1',
    'description': 'Extract plain text from HTML',
    'long_description': '# Extract plain text from HTML\n\n## Installation\n\n```\n$ pip install plainhtml\n```\n\n## Example\n\n```python\n>>> import plainhtml\n>>> html = "<html><body><p>foo</p><p>bar</p></body></html>"\n>>> plainhtml.extract(html)\n\'foo\\n\\nbar\'\n```\n',
    'author': 'Severin Simmler',
    'author_email': 's.simmler@snapaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
