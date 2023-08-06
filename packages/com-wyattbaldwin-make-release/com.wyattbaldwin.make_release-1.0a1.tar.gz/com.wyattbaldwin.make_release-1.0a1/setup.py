# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['make_release']

package_data = \
{'': ['*']}

install_requires = \
['runcommands>=1.0a62,<2.0']

entry_points = \
{'console_scripts': ['make-release = make_release:make_release.console_script']}

setup_kwargs = {
    'name': 'com.wyattbaldwin.make-release',
    'version': '1.0a1',
    'description': 'Make a release',
    'long_description': '# Make a Release\n\nMake a release\n\n## Usage\n\n    make-release\n\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wylee/com.wyattbaldwin/tree/dev/make_release',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
