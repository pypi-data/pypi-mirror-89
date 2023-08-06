# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrogram_to_audio',
 'spectrogram_to_audio.config',
 'spectrogram_to_audio.data_preprocessing',
 'spectrogram_to_audio.tests']

package_data = \
{'': ['*'],
 'spectrogram_to_audio.config': ['config_files/*'],
 'spectrogram_to_audio.tests': ['audios/*']}

install_requires = \
['dynaconf>=3.1.2,<4.0.0',
 'tensorflow-addons>=0.11.2,<0.12.0',
 'tensorflow-datasets>=4.1.0,<5.0.0',
 'tensorflow-io>=0.16.0,<0.17.0',
 'tensorflow>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'spectrogram-to-audio',
    'version': '0.0.5',
    'description': '',
    'long_description': None,
    'author': 'carl2g',
    'author_email': 'degentilecarl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
