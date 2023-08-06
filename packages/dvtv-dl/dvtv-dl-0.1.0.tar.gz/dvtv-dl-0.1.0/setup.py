# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dvtv_dl']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.2,<7.0.0', 'youtube_dl>=2020.12.29,<2021.0.0']

entry_points = \
{'console_scripts': ['dvtv-dl = dvtv_dl']}

setup_kwargs = {
    'name': 'dvtv-dl',
    'version': '0.1.0',
    'description': '',
    'long_description': 'DVTV downloader\n===============\n\nInstallation\n------------\n\n    pip install dvtv-dl\n\nUsage\n-----\n\n    dvtv-dl\n',
    'author': 'Jakub Dorňák',
    'author_email': 'jakub.dornak@misli.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/misli/dvtv-dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
