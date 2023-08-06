# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['baluchon', 'baluchon.validator']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2==2.11.2',
 'cerberus==1.3.2',
 'clickhouse-cityhash==1.0.2.3',
 'clickhouse-driver==0.1.4',
 'lz4==3.1.0',
 'pendulum==2.1.2']

setup_kwargs = {
    'name': 'baluchon',
    'version': '0.0.1',
    'description': 'A tool for managing migrations in Clickhouse',
    'long_description': '# [WIP] Clickhouse Migration \n\nCurrently, in active development\n\nA Clickhouse migration tools written in Python.\n\nA tool to manage migrations on Clickhouse using clickhouse-driver\n\n## Inspirations\ngolang-migrate\n\n## Features\n- Support data replication\n\n## TODO\n- Tests\n- Support prefetching migrations for heavy sources\n- Add S3 Source\n- Add doc\n- Complete exceptions\n- Replace cerberus by pydantic\n- Implement the graceful stop (finish operations if cancel is requested)',
    'author': 'Alain BERRIER',
    'author_email': 'alain.berrier@outlook.com',
    'maintainer': 'Alain BERRIER',
    'maintainer_email': 'alain.berrier@outlook.com',
    'url': 'https://gitlab.com/aberrier/baluchon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
