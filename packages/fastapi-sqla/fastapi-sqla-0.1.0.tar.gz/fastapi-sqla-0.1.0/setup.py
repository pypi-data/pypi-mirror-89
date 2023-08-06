# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fastapi_sqla']
install_requires = \
['fastapi>=0.61', 'psycopg2<3', 'sqlalchemy<2', 'structlog>=20']

setup_kwargs = {
    'name': 'fastapi-sqla',
    'version': '0.1.0',
    'description': 'SqlAlchemy integration for FastAPI®',
    'long_description': None,
    'author': 'Hadrien David',
    'author_email': 'hadrien.david@dialogue.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
