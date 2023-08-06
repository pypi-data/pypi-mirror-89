# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chalky', 'chalky.interface', 'chalky.shortcuts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chalky',
    'version': '0.1.0',
    'description': 'Simple ANSI terminal text coloring',
    'long_description': '# Chalky\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/chalky.svg)](https://pypi.org/project/chalky/)\n[![Test Status](https://github.com/stephen-bunn/chalky/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/chalky)\n[![Documentation Status](https://readthedocs.org/projects/chalky/badge/?version=latest)](https://chalky.readthedocs.io/)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> Simple ANSI terminal text coloring\n\n```python\nfrom chalky import sty, fg\n\nmy_style = sty.bold & fg.red\nprint(my_style | "This is red on black")\nprint(my_style.reverse | "This is black on red")\n```\n\n![Basic Colors](docs/source/_static/assets/img/basic.png)\n\n```python\nfrom chalky import rgb, sty, hex\n\nprint(rgb(23, 255, 122) & sty.italic | "Truecolor as well")\nprint(sty.bold & hex("#ff02ff") | "More and more colors")\n```\n\n![True Colors](docs/source/_static/assets/img/truecolor.png)\n',
    'author': 'Stephen Bunn',
    'author_email': 'stephen@bunn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephen-bunn/chalky',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
