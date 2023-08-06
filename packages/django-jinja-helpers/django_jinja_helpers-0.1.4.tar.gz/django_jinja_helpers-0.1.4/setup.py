# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_jinja_helpers', 'django_jinja_helpers.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django-crispy-forms>=1.10.0,<2.0.0',
 'django-jinja>=2.7.0,<3.0.0',
 'django-webpack-loader>=0.7.0,<0.8.0',
 'django>=3.1.4,<4.0.0']

setup_kwargs = {
    'name': 'django-jinja-helpers',
    'version': '0.1.4',
    'description': 'Helpers for using django-jinja',
    'long_description': 'Django Jinja Helpers\n====================\n\nHelpers for using django-jinja (https://github.com/niwinz/django-jinja) with\n\n- django-crisp-forms\n- django-webpack-loader\n\nInstallation\n------------\n\nTo get the latest stable release from PyPi\n\n.. code-block:: bash\n\n    pip install django_jinja_helpers\n\nInstall the app\n\n.. code-block:: python\n\n    INSTALLED_APPS = (\n        ...,\n        \'django_jinja_helpers\',\n    )\n\nUsage\n-----\n\nCall ``render_bundle()`` in your template\n\n.. code-block:: html\n\n    <!DOCTYPE html>\n    <html>\n      <head>\n        {{ render_bundle(\'styles\', \'css\') }}\n      </head>\n\n      <body>\n      </body>\n    </html>\n\nCall ``crispy()`` in your template\n\n.. code-block:: html\n\n    <div class="container">\n      {{ crispy(form) }}\n    </div>\n',
    'author': 'Enrico Barzetti',
    'author_email': 'enricobarzetti@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enricobarzetti/django_jinja_helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
