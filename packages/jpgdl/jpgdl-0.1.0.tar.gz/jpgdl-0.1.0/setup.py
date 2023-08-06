# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jpgdl']
install_requires = \
['Pillow>=8.0.1,<9.0.0', 'httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'jpgdl',
    'version': '0.1.0',
    'description': 'Just a simple script and library image downloader and saving it in JPEG format.',
    'long_description': '# jpgdl\n\nJust a simple script and library image downloader and saving it in JPEG format.\n',
    'author': 'TheBoringDude',
    'author_email': 'iamcoderx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheBoringDude/jpgdl',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
