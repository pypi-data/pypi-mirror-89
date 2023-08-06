# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_auth_multitoken', 'rest_auth_multitoken.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django-rest-auth>=0.9.5,<0.10.0']

setup_kwargs = {
    'name': 'rest-auth-multitoken',
    'version': '0.2.2',
    'description': 'Add multiple tokens support to django-rest-auth.',
    'long_description': "# Rest Auth Multitoken\n\n[django-rest-auth](https://github.com/Tivix/django-rest-auth) is a great package \nfor authentication with django, however it lacks the possibility of allowing a user\n to have multiple auth tokens. Thus a user has a single token shared across all his\n  clients, and when he logs out from one client he gets logged out of all his clients.\n\nrest-auth-multitoken solves this problem by adding  multiple tokens support for a single user to django-rest-auth.\n\n# Installation\n\ninstall `rest-auth-multitoken`\n```\n> pip install rest-auth-multitoken\n```\n\nThen in django's `settings.py`:\n\nadd it to `INSTALLED_APPS`: \n```py\n# settings.py\nINSTALLED_APPS = [\n    ...\n    'rest_auth_multitoken',\n    ...\n]\n```\n\nadd it to `REST_FRAMEWORK`'s  config:\n\n```py\n# settings.py\n\nREST_FRAMEWORK = {\n    'DEFAULT_AUTHENTICATION_CLASSES': (\n        ...\n        'rest_auth_multitoken.utils.MultiTokenAuthentication',\n        ...\n    ),\n}\n\n```\n\nconfigure `django-rest-auth` to use `rest-auth-multitoken`:\n```py\n# settings.py\nREST_AUTH_TOKEN_CREATOR = 'rest_auth_multitoken.utils.multitoken_create'\nREST_AUTH_TOKEN_MODEL = 'rest_auth_multitoken.models.Token'\n```\n\nFinally include the new `MultitokenLogoutView` and `MultitokenRegisterView` in `urls.py`, just before `django-rest-auth`'s urls:\n\n```py\n# urls.py\nfrom rest_auth_multitoken.views import (\n    MultitokenRegisterView,\n    MultitokenLogoutView,\n)\n\n\n\nurlpatterns = [\n    ...\n    path('api/auth/logout/', MultitokenLogoutView.as_view()),\n    path('api/auth/registration/', MultitokenRegisterView.as_view())\n\n    path('api/auth/registration/', include('rest_auth.registration.urls'))\n    path('api/auth/', include('rest_auth.urls')),\n    ...\n]\n```\n\nNow everytime a user logs in he'll get a new token, even if he's logged in from another client.",
    'author': 'makerGeek',
    'author_email': 'moetez.93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/makerGeek/rest-auth-multitoken',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
