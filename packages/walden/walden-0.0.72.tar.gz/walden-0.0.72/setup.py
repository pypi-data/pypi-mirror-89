# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['walden', 'walden.compiler', 'walden.journal', 'walden.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['walden = walden.__main__:main']}

setup_kwargs = {
    'name': 'walden',
    'version': '0.0.72',
    'description': 'A .tex journal system',
    'long_description': '# Goal\n\nDevelop a simple automated journaling system that removes the pain points of maintenance and\norganization, allowing the user to focus on writing. \n\n# Install\n\nAvailable via pip: `pip install walden`\n\n# Usage\n\nWalden will create a `journals/` folder in your home directory. This is where all your output and\n.tex files will be stored. The commands are:\n\n| Flag                  | Description                    |\n|-----------------------|--------------------------------|\n| walden -h                    | show help dialog               |\n| walden delete <journal name> | Delete an existing journal     |\n| walden today <journal name>  | New entry in specified journal |\n| walden list                  | List names of journals         |\n| walden build <journal name>  | Compile journal as .pdf        |\n| walden view <journal name>   | View journal as .pdf           |\n\n\n# TODO:\n-  better support for journal names with spaces (replace " " with _ for path)\n-  better cli support using click or argparse\n-  change path where journals are stored\n-  allow journal import/export\n-  plug-in system for things like weather/question of the day\n\n\n',
    'author': 'Aravind Koneru',
    'author_email': 'aravind.b.koneru@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aravindkoneru/walden',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
