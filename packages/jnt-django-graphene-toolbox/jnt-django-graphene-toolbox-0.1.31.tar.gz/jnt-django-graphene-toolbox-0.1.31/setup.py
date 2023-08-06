# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jnt_django_graphene_toolbox',
 'jnt_django_graphene_toolbox.connection_fields',
 'jnt_django_graphene_toolbox.connection_fields.mixins',
 'jnt_django_graphene_toolbox.converters',
 'jnt_django_graphene_toolbox.errors',
 'jnt_django_graphene_toolbox.filters',
 'jnt_django_graphene_toolbox.filters.mixins',
 'jnt_django_graphene_toolbox.helpers',
 'jnt_django_graphene_toolbox.mutations',
 'jnt_django_graphene_toolbox.security.mixins',
 'jnt_django_graphene_toolbox.security.permissions',
 'jnt_django_graphene_toolbox.serializers',
 'jnt_django_graphene_toolbox.serializers.fields',
 'jnt_django_graphene_toolbox.serializers.validators',
 'jnt_django_graphene_toolbox.types',
 'jnt_django_graphene_toolbox.views']

package_data = \
{'': ['*'],
 'jnt_django_graphene_toolbox': ['locale/en/LC_MESSAGES/*',
                                 'locale/ru/LC_MESSAGES/*']}

install_requires = \
['django-filter',
 'djangorestframework',
 'graphene-file-upload',
 'graphene_django',
 'jnt_django_toolbox']

setup_kwargs = {
    'name': 'jnt-django-graphene-toolbox',
    'version': '0.1.31',
    'description': '',
    'long_description': None,
    'author': 'Junte',
    'author_email': 'tech@junte.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
