# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ringkasan', 'ringkasan.core']

package_data = \
{'': ['*']}

install_requires = \
['fastai>=2.1.9,<3.0.0',
 'ipykernel>=5.4.2,<6.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.4,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'tensorflow-text>=2.4.1,<3.0.0',
 'tensorflow>=2.4.0,<3.0.0']

entry_points = \
{'console_scripts': ['ringkasan-hello = ringkasan:hello']}

setup_kwargs = {
    'name': 'ringkasan',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Ringkasan\n\nExplore different ways to consume a website by converting it into different medium\n\n## Developer Setup\n\n### Publish\n\n```\npoetry build && poetry publish\n```\n',
    'author': 'jinified',
    'author_email': 'jinified@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
