# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_framework_apicontrol', 'rest_framework_apicontrol.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>2.2', 'djangorestframework>3.7.0', 'psycopg2-binary>=2.8.2']

setup_kwargs = {
    'name': 'rest-framework-apicontrol',
    'version': '0.8.2',
    'description': 'Control Clients Apps access over REST APIs with ApiKeys',
    'long_description': '# djangorestframework-apicontrol\n\nThis is an App intended to control Clients Apps access over REST APIs.\n\n## Notice\n```\nPlease be carefull with the use of this package, and remember to backup your database before apply each migration.\n```\n\n## Permission Usage (APIKey)\nyou only has to import the permission and use it in your rest_framework views, or in your settings.py file, as you prefer. e.g:\n\n``` python\n"""Contact views."""\nfrom rest_framework import viewsets\nfrom rest_framework_apicontrol.permissions import HasApiKeyPermission\nfrom .models import (\n    ContactInfo\n)\nfrom .serializers import (\n    ContactInfoSerializer\n)\n\n\nclass ContactInfoViewSet(viewsets.ModelViewSet):\n    queryset = ContactInfo.objects.all()\n    serializer_class = ContactInfoSerializer\n    permission_classes = [HasApiKeyPermission]\n    authentication_classes = []\n\n```\n\nAll the calls to this endpoint **MUST HAVE** a header called **Api-Key** with the value of an App(App model in Django admin site)\n\n## Models\nThis app comes with several models & mixins which provide useful common fields & functions, the models it provides are the following:\n\n![models diagram](docs/img/models.png)\n\nTo add those models to your app the only you need to do is add `rest_framework_apicontrol` to your project `INSTALLED_APPS` setting & then migrate your app.\n``` python\nINSTALLED_APPS = [\n    # Django default modules\n    \'django.contrib.admin\',\n    \'django.contrib.auth\',\n    \'django.contrib.contenttypes\',\n    \'django.contrib.sessions\',\n    \'django.contrib.messages\',\n    \'django.contrib.staticfiles\',\n    # Security & multi-app management\n    \'rest_framework_apicontrol\',\n    # Your project apps\n    \'...\',\n]\n```\n\n**Notice:** This project\'s models needs PostgreSQL as database because the use of JSONField in some of it\'s model fields.\n\n\n## Donate\nIf this project is useful for you, please donate some dollars to help me improve this & others projects.\n\nMy Paypal - http://paypal.me/mcuetodeveloper\n',
    'author': 'Marcelo Cueto',
    'author_email': 'cueto@live.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
