# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instasave']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.4.1,<0.5.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.46.0,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['instasave = instasave.__main__:app']}

setup_kwargs = {
    'name': 'instasave',
    'version': '0.2.0',
    'description': 'Download script for Instagram posts',
    'long_description': '<h1 align="center">\n  <b>instasave</b>\n</h1>\n\nA simple script to download media from Instagram posts.\n\n## Install\n\nThis script runs on Python3.6+.\nYou can install it from PyPI with:\n```bash\npip install instasave\n```\n\n## Usage\n\nWith this package installed in the activated enrivonment, it can be called through `python -m instasave` or through a newly created `instasave` command.\n\nDetailed usage goes as follows:\n```bash\nUsage: instasave [OPTIONS] [URL]\n\n  Download media from Instagram posts.\n\nArguments:\n  [URL]  Link to the Instagram post you want to download the content of.\n\nOptions:\n  --log-level TEXT      The base console logging level. Can be \'debug\',\n                        \'info\', \'warning\' and \'error\'.  [default: info]\n\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n\n  --help                Show this message and exit.\n```\n\nThe downloaded files will be saved in the current directory under a name composed of the file type (image / video) appended by the download timestamp.\n\nWarning: abusing this script may get your IP banned by Instagram.\n\n## TODO\n\n- [x] Implement proper logging.\n- [x] Make into a package.\n- [x] Make callable as a python module (`python -m instasave ...`).\n- [x] Improving the command line experience.\n\n## License\n\nCopyright &copy; 2020 Felix Soubelet. [MIT License][license]\n\n[license]: https://github.com/fsoubelet/InstaSave/blob/master/LICENSE\n[loguru_url]: https://github.com/Delgan/loguru\n[requests_url]: https://github.com/psf/requests\n[tqdm_url]: https://github.com/tqdm/tqdm\n',
    'author': 'Felix Soubelet',
    'author_email': 'felix.soubelet@liverpool.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsoubelet/InstaSave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
