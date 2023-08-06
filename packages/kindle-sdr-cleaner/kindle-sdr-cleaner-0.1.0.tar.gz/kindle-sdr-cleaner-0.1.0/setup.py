# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kindle_sdr_cleaner']
entry_points = \
{'console_scripts': ['kindle-sdr-cleaner = kindle_sdr_cleaner:main']}

setup_kwargs = {
    'name': 'kindle-sdr-cleaner',
    'version': '0.1.0',
    'description': 'Clean useless .sdr folders in your Kindle.',
    'long_description': '# Kindle SDR Cleaner\n\nClean useless `.sdr` folders in your Kindle.\n\n## Installation\n\n```bash\npipx install kindle-sdr-cleaner\n```\n\n## Usage\n\n```bash\nkindle-sdr-cleaner # clean in current folder\nkindle-sdr-cleaner /Volumes/Kindle # clean in /Volumes/Kindle\n```\n',
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/kindle-sdr-cleaner',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
