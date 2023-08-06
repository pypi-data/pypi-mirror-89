# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['staticfiles_downloader']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0,<4']

setup_kwargs = {
    'name': 'django-staticfiles-downloader',
    'version': '1.0.0',
    'description': 'Django staticfiles extension to download third-party static files',
    'long_description': "-----------------------------\ndjango-staticfiles-downloader\n-----------------------------\n\n``django-staticfiles-downloader`` provides ``staticfiles_downloader.DownloaderFinder``,\nan extension of ``django.contrib.staticfiles``, which allows you to specify static files\nwith urls and optionaly checksum in your Django application or Django project settings.\nThis is particularly useful, when using third-party static files, if you don't want to\neither include the files in your project nor depend on CDN in runtime.\n\nThe static files are collected with ``python manage.py collectstatic``.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    pip install  django-staticfiles-downloader\n\n\nConfiguration\n-------------\n\nAdd ``staticfiles_downloader.DownloaderFinder`` to ``settings.STATICFILES_FINDERS``:\n\n.. code-block:: python\n\n    STATICFILES_FINDERS = [\n        'django.contrib.staticfiles.finders.FileSystemFinder',\n        'django.contrib.staticfiles.finders.AppDirectoriesFinder',\n        'staticfiles_downloader.DownloaderFinder',\n    ]\n\nDefine static files urls in your Django application\n...................................................\n\n.. code-block:: python\n\n    # your_app/__init__.py\n    staticfiles_urls = {\n        # use only url\n        'my_app/js/jquery-3.2.1.min.js': 'https://code.jquery.com/jquery-3.2.1.min.js',\n        # or use url and checksum\n        'my_app/js/jquery-2.2.4.min.js': (\n            'https://code.jquery.com/jquery-2.2.4.min.js',\n            'sha384',\n            'rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB',\n        ),\n    }\n\nDefine static files urls in your Django project settings\n........................................................\n\n.. code-block:: python\n\n    # your_project/settings.py\n    STATICFILES_URLS = {\n        # use only url\n        'js/jquery-3.2.1.min.js': 'https://code.jquery.com/jquery-3.2.1.min.js',\n        # or use url and checksum\n        'js/jquery-2.2.4.min.js': (\n            'https://code.jquery.com/jquery-2.2.4.min.js',\n            'sha384',\n            'rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB',\n        ),\n    }\n",
    'author': 'Jakub Dorňák',
    'author_email': 'jakub.dornak@misli.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/misli/django-staticfiles-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
