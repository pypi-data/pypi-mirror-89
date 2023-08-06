# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['runcommands',
 'runcommands.commands',
 'runcommands.completion',
 'runcommands.util']

package_data = \
{'': ['*'], 'runcommands.completion': ['bash/*', 'fish/*']}

install_requires = \
['Jinja2>=2.10,<3.0', 'PyYAML>=5.1,<6.0', 'blessings>=1.7,<2.0']

entry_points = \
{'console_scripts': ['run = runcommands.__main__:main',
                     'runcommand = runcommands.__main__:main',
                     'runcommands = runcommands.__main__:main',
                     'runcommands-complete = '
                     'runcommands.completion:complete.console_script',
                     'runcommands-complete-base-command = '
                     'runcommands.completion:complete_base_command.console_script']}

setup_kwargs = {
    'name': 'runcommands',
    'version': '1.0a63',
    'description': 'A framework for writing console scripts and running commands',
    'long_description': None,
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://runcommands.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
