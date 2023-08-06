# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seaport']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['seaport = seaport.console:main']}

setup_kwargs = {
    'name': 'seaport',
    'version': '0.1.0',
    'description': 'A more mighty port bump',
    'long_description': '# 🌊 seaport\n\n*A more mighty `port bump` for MacPorts!*\n\n![](./images/gping.gif)\n\n*⚠️ This program is very early on in development, and is still currently being built. Watch this space! ⚠️*\n\nEffortlessly bumps version numbers and checksums for MacPorts portfiles, copies the changes to your clipboard, and optionally sends a PR to update them.\n\n## ⬇️ Install\n\nNote that if installing from PyPi or building from source, [MacPorts](https://www.macports.org/) needs to already be installed, and [GitHub CLI](https://cli.github.com/) is required if using the `--pr` flag.\n\n### PyPi\n\n```\npip install seaport\n```\n\n### Build from source\n\n```\ngit clone https://github.com/harens/seaport\ncd seaport\npoetry install\npoetry shell\nseaport\n```\n\n## 💻 Usage\n\n```txt\n> seaport --help\nUsage: seaport [OPTIONS] NAME\n\n  Bumps the version number and checksum of NAME, and copies the result to\n  your clipboard\n\nOptions:\n  --version                 Show the version and exit.\n  --bump TEXT               The new version number\n  --pr PATH                 Location for where to clone the macports-ports\n                            repo\n\n  --test / --no-test        Runs port test\n  --lint / --no-lint        Runs port lint --nitpick\n  --install / --no-install  Installs the port and allows testing of basic\n                            functionality\n\n  --help                    Show this message and exit.\n```\n\n### 🚀 Use of sudo\n\nSudo is only required if `--test`, `--lint` or `--install` are specified, and it will be asked for during runtime. This is since the local portfile repo needs to be modified to be able to run the relevant commands.\n\nAny changes made to the local portfile repo are reverted during the cleanup stage.\n\n## 🔨 Contributing\n\nAny change, big or small, that you think can help improve this action is more than welcome 🎉.\n\nAs well as this, feel free to open an issue with any new suggestions or bug reports. Every contribution is appreciated.\n\n## 📒 Notice of Non-Affiliation and Disclaimer\n\n<img src="https://avatars2.githubusercontent.com/u/4225322?s=280&v=4" align="right"\n     alt="MacPorts Logo" width="150">\n\nThis project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the MacPorts Project, or any of its subsidiaries or its affiliates. The official MacPorts Project website can be found at <https://www.macports.org>.\n\nThe name MacPorts as well as related names, marks, emblems and images are registered trademarks of their respective owners.\n',
    'author': 'harens',
    'author_email': 'harensdeveloper@gmail.com',
    'maintainer': 'harens',
    'maintainer_email': 'harensdeveloper@gmail.com',
    'url': 'https://github.com/harens/seaport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
