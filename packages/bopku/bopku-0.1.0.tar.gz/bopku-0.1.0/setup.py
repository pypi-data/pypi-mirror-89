# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bopku', 'bopku.alembic', 'bopku.alembic.versions', 'bopku.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<2.0.0', 'alembic>=1.4.3,<2.0.0', 'dacite>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'bopku',
    'version': '0.1.0',
    'description': 'Alat bantu administrasi BOP (Bantuan Operasional) Paud.',
    'long_description': '# Bopku\n\nBopku merupakan alat bantu administrasi BOP Paud.\n\n## Fitur yang akan datang\n\nBerikut fitur yang akan direncanakan untuk aplikasi ini.\n\n- Export ke excel\n- Export ke word\n- Print Kwitansi\n\n## Donasi\n\nJika anda ingin melakukan donasi untuk kami, bisa menghubungi kami melalui [WhatsApp](https://wa.me/6287725780404) ataupun [Telegram](https://t.me/hexatester).\n\n## Legal / Hukum\n\nKode ini sama sekali tidak berafiliasi dengan, diizinkan, dipelihara, disponsori atau didukung oleh Kemdikbud atau afiliasi atau anak organisasinya. Ini adalah perangkat lunak yang independen dan tidak resmi. _Gunakan dengan risiko Anda sendiri_.\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dapodix.github.io/bopku/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
