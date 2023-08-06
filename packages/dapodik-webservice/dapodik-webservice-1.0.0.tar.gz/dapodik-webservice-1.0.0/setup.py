# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dapodik_webservice',
 'dapodik_webservice.models',
 'dapodik_webservice.models.ptk',
 'dapodik_webservice.models.rombongan_belajar']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dapodik-webservice',
    'version': '1.0.0',
    'description': 'SDK Python Web Service aplikasi Dapodik',
    'long_description': '# dapodik-webservice\n\n[![dapodik-webservice - PyPi](https://img.shields.io/pypi/v/dapodik-webservice)](https://pypi.org/project/dapodik-webservice/)\n\nSDK Python Web Service aplikasi Dapodik\n\n## Install\n\nPastikan python 3.7 terinstall, kemudian jalankan perintah di bawah dalam Command Prompt atau Powershell (di Windows + X):\n\n```bash\npip install --upgrade dapodik\n```\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh Kemdikbud atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. Gunakan dengan risiko Anda sendiri.\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dapodix.github.io/dapodik-webservice/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
