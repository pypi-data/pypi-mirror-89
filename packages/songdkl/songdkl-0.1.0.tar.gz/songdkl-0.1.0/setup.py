# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['songdkl', 'songdkl.argparser']

package_data = \
{'': ['*']}

install_requires = \
['mahotas>=1.4.11,<2.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'scipy>=1.5.4,<2.0.0']

entry_points = \
{'console_scripts': ['songdkl = songdkl.__main__:main']}

setup_kwargs = {
    'name': 'songdkl',
    'version': '0.1.0',
    'description': 'automated quantitation of vocal learning in songbirds',
    'long_description': None,
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
