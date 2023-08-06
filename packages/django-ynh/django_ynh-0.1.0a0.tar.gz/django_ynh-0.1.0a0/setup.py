# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_ynh', 'django_ynh.sso_auth']

package_data = \
{'': ['*']}

install_requires = \
['django', 'django-axes', 'django-redis', 'psycopg2-binary']

entry_points = \
{'console_scripts': ['publish = django_ynh_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'django-ynh',
    'version': '0.1.0a0',
    'description': 'Glue code to package django projects as yunohost apps.',
    'long_description': "# django_ynh\n\nCurrent state is broken, because we are **planing** ;)\n\n[![Integration level](https://dash.yunohost.org/integration/django_ynh.svg)](https://dash.yunohost.org/appci/app/django_ynh) ![](https://ci-apps.yunohost.org/ci/badges/django_ynh.status.svg) ![](https://ci-apps.yunohost.org/ci/badges/django_ynh.maintain.svg)\n[![Install django_ynh with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=django_ynh)\n\n> *This package allows you to install django_ynh quickly and simply on a YunoHost server.\nIf you don't have YunoHost, please consult [the guide](https://yunohost.org/#/install) to learn how to install it.*\n\nPull requests welcome ;)\n\n## Overview\n\nGlue code to package django projects as yunohost apps.\n\n## SSO authentication\n\n[SSOwat](https://github.com/YunoHost/SSOwat) is fully supported:\n\n* First user (`$YNH_APP_ARG_ADMIN`) will be created as Django's super user\n* All new users will be created as normal users\n* Login via SSO is fully supported\n* User Email, First / Last name will be updated from SSO data\n\n\n## Links\n\n * Report a bug about this package: https://github.com/YunoHost-Apps/django_ynh\n * YunoHost website: https://yunohost.org/\n\n---\n\n# Developer info\n\n## package installation / debugging\n\nPlease send your pull request to https://github.com/YunoHost-Apps/django_ynh\n\nTry 'main' branch, e.g.:\n```bash\nsudo yunohost app install https://github.com/YunoHost-Apps/django_ynh/tree/master --debug\nor\nsudo yunohost app upgrade django_ynh -u https://github.com/YunoHost-Apps/django_ynh/tree/master --debug\n```\n\nTry 'testing' branch, e.g.:\n```bash\nsudo yunohost app install https://github.com/YunoHost-Apps/django_ynh/tree/testing --debug\nor\nsudo yunohost app upgrade django_ynh -u https://github.com/YunoHost-Apps/django_ynh/tree/testing --debug\n```\n\nTo remove call e.g.:\n```bash\nsudo yunohost app remove django_ynh\n```\n\nBackup / remove / restore cycle, e.g.:\n```bash\nyunohost backup create --apps django_ynh\nyunohost backup list\narchives:\n  - django_ynh-pre-upgrade1\n  - 20201223-163434\nyunohost app remove django_ynh\nyunohost backup restore 20201223-163434 --apps django_ynh\n```\n\nDebug installation, e.g.:\n```bash\nroot@yunohost:~# ls -la /var/www/django_ynh/\ntotal 18\ndrwxr-xr-x 4 root root 4 Dec  8 08:36 .\ndrwxr-xr-x 6 root root 6 Dec  8 08:36 ..\ndrwxr-xr-x 2 root root 2 Dec  8 08:36 media\ndrwxr-xr-x 7 root root 8 Dec  8 08:40 static\n\nroot@yunohost:~# ls -la /opt/yunohost/django_ynh/\ntotal 58\ndrwxr-xr-x 5 django_ynh django_ynh   11 Dec  8 08:39 .\ndrwxr-xr-x 3 root        root           3 Dec  8 08:36 ..\n-rw-r--r-- 1 django_ynh django_ynh  460 Dec  8 08:39 gunicorn.conf.py\n-rw-r--r-- 1 django_ynh django_ynh    0 Dec  8 08:39 local_settings.py\n-rwxr-xr-x 1 django_ynh django_ynh  274 Dec  8 08:39 manage.py\n-rw-r--r-- 1 django_ynh django_ynh  171 Dec  8 08:39 secret.txt\ndrwxr-xr-x 6 django_ynh django_ynh    6 Dec  8 08:37 venv\n-rw-r--r-- 1 django_ynh django_ynh  115 Dec  8 08:39 wsgi.py\n-rw-r--r-- 1 django_ynh django_ynh 4737 Dec  8 08:39 django_ynh.settings.py\n\nroot@yunohost:~# cd /opt/yunohost/django_ynh/\nroot@yunohost:/opt/yunohost/django_ynh# source venv/bin/activate\n(venv) root@yunohost:/opt/yunohost/django_ynh# ./manage.py check\ndjango_ynh v0.8.2 (Django v2.2.17)\nDJANGO_SETTINGS_MODULE='django_ynh.settings'\nPROJECT_PATH:/opt/yunohost/django_ynh/venv/lib/python3.7/site-packages\nBASE_PATH:/opt/yunohost/django_ynh\nSystem check identified no issues (0 silenced).\n\nroot@yunohost:~# tail -f /var/log/django_ynh/django_ynh.log\nroot@yunohost:~# cat /etc/systemd/system/django_ynh.service\n\nroot@yunohost:~# systemctl reload-or-restart django_ynh\nroot@yunohost:~# journalctl --unit=django_ynh --follow\n```\n\n## local test\n\nFor quicker developing of django_ynh in the context of YunoHost app,\nit's possible to run the Django developer server with the settings\nand urls made for YunoHost installation.\n\ne.g.:\n```bash\n~$ git clone https://github.com/YunoHost-Apps/django_ynh.git\n~$ cd django_ynh/\n~/django_ynh$ make\ninstall-poetry         install or update poetry\ninstall                install django_ynh via poetry\nupdate                 update the sources and installation\nlocal-test             Run local_test.py to run django_ynh locally\n~/django_ynh$ make install-poetry\n~/django_ynh$ make install\n~/django_ynh$ make local-test\n```\n\nNotes:\n\n* SQlite database will be used\n* A super user with username `test` and password `test` is created\n* The page is available under `http://127.0.0.1:8000/app_path/`\n",
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
