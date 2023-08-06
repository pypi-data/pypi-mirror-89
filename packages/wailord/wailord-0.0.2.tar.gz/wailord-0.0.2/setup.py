# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wailord', 'wailord.exp', 'wailord.io']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'Pint-Pandas>=0.1,<0.2',
 'Pint>=0.16.1,<0.17.0',
 'Sphinx>=3.3.1,<4.0.0',
 'ase>=3.20.1,<4.0.0',
 'black>=20.8b1,<21.0',
 'click>=7.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'flake8>=3.8.4,<4.0.0',
 'konfik>=2.0.0,<3.0.0',
 'pandas>=1.1.3,<2.0.0',
 'parsimonious>=0.8.1,<0.9.0',
 'pytest-datadir>=1.3.1,<2.0.0',
 'releases>=1.6.3,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'siuba>=0.0.24,<0.0.25',
 'sphinx-autobuild>=2020.9.1,<2021.0.0',
 'sphinx-comments>=0.0.3,<0.0.4',
 'sphinx-copybutton>=0.3.1,<0.4.0',
 'sphinx-fasvg>=0.1.3,<0.2.0',
 'sphinx-issues>=1.2.0,<2.0.0',
 'sphinx-library>=1.1.2,<2.0.0',
 'sphinx-minipres>=0.2.1,<0.3.0',
 'sphinx-proof>=0.0.3,<0.0.4',
 'sphinx-sitemap>=2.2.0,<3.0.0',
 'sphinx-togglebutton>=0.2.3,<0.3.0',
 'sphinx-versions>=1.1.3,<2.0.0',
 'sphinxcontrib-apidoc>=0.3.0,<0.4.0',
 'sphinxcontrib-doxylink>=1.6.1,<2.0.0',
 'sphinxcontrib-github_ribbon>=0.9.0,<0.10.0',
 'sphinxcontrib.contributors>=1.0,<2.0',
 'vg>=1.9.0,<2.0.0']

entry_points = \
{'console_scripts': ['run = wailord.cli:main']}

setup_kwargs = {
    'name': 'wailord',
    'version': '0.0.2',
    'description': 'Wailord is a python library to interact with ORCA',
    'long_description': '=======\nWailord\n=======\n\n.. image:: https://w.wallhaven.cc/full/4x/wallhaven-4xgw53.jpg\n        :alt: Logo of sorts\n\n.. image:: https://img.shields.io/pypi/v/wailord.svg\n        :target: https://pypi.python.org/pypi/wailord\n\n.. image:: https://zenodo.org/badge/303189277.svg\n        :target: https://zenodo.org/badge/latestdoi/303189277\n        :alt: Zenodo Status\n\n.. image:: https://img.shields.io/travis/HaoZeke/wailord.svg\n        :target: https://travis-ci.com/HaoZeke/wailord\n\n.. image:: https://api.netlify.com/api/v1/badges/2209e709-8d41-46ee-bf4d-0b116f9243b1/deploy-status\n        :target: https://app.netlify.com/sites/wailord/deploys\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/HaoZeke/wailord/shield.svg\n     :target: https://pyup.io/repos/github/HaoZeke/wailord/\n     :alt: Updates\n\n\nWailord is a python library to interact with ORCA_\n\n\n* Free software: GNU General Public License v3\n* Documentation: https://wailord.xyz\n\nBeing written up. Till then feel free to use the ZenodoDOI_.\n\n\nFeatures\n--------\n\n* Integrates with SLURM in a manner of speaking\n* Generic helpers for building arbitrary input files\n* Generates data-frames for all supported runs\n\nLimitations\n-----------\n\n* By choice, the split-job syntax has not been included\n\nCredits\n-------\n\n* Initially conceived during EFN115F_\n* This package was based off the `audreyr/cookiecutter-pypackage`_ Cookiecutter_ template\n* The image is from `wallhaven.cc`_\n* The favicon is from Bulbagarden_\n\n.. _ORCA: https://orcaforum.kofo.mpg.de/\n.. _EFN115F: https://notendur.hi.is/~hj/reikniefnafr/\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n.. _ZenodoDOI: https://zenodo.org/badge/latestdoi/303189277\n.. _Bulbagarden: https://archives.bulbagarden.net/wiki/File:321Wailord_AG_anime.png\n.. _`wallhaven.cc`: https://wallhaven.cc/w/4xgw53\n',
    'author': 'Rohit Goswami',
    'author_email': 'rog32@hi.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wailord.xyz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
