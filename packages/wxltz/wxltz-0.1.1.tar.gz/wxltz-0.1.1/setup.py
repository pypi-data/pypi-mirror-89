# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wxltz']

package_data = \
{'': ['*']}

install_requires = \
['pywal>=3.3.0,<4.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['waltz = wxltz.main:app']}

setup_kwargs = {
    'name': 'wxltz',
    'version': '0.1.1',
    'description': '',
    'long_description': '# wxltz\n\nA pywal wrapper CLI\n\n> [TODO]: Add docs\n',
    'author': 'givonwash',
    'author_email': 'givonwash@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
