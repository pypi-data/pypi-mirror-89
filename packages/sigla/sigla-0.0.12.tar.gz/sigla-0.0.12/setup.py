# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sigla',
 'sigla.lib',
 'sigla.lib.Nodes',
 'sigla.lib.Nodes.template',
 'sigla.lib.Nodes.template.engines',
 'sigla.lib.helpers']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.1.2,<8.0.0',
 'flake8>=3.8.4,<4.0.0',
 'mypy>=0.790,<0.791',
 'pydash>=4.9.1,<5.0.0',
 'python-frontmatter>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['sigla = sigla_cli.cli:cli']}

setup_kwargs = {
    'name': 'sigla',
    'version': '0.0.12',
    'description': '',
    'long_description': None,
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
