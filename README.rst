======
SvnLab
======

SvnLab is a simple Django app to manage svn server. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Get svnlab::

    git clone https://github.com/jiuchou/svnlab.git -b develop

2. Change configuration::

    Update Ldap configuration:
        svnlab.user.management

    Replace the following file contents with valid file contents::

            # auth file for svn
            svnlab/svnlab/common/roleUtils/dav_svn.authz
            # manager, url
            svnlab/svnlab/common/roleUtils/managerToUrl
            # module, prefixUrl
            svnlab/svnlab/common/roleUtils/prefixUrl

3. Create Database in MySQL Database::

    CREATE DATABASE svnlab DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

4. Install svnlab as a library for Python::

    make install

5. Run `python manage.py makemigrations` to create the app migrations::

    Modify svnlab.setting:
        Change default database host "127.0.0.1" to wanted database host

    python manage.py makemigrations user
    python manage.py makemigrations svn

6. Run `python manage.py migrate` to create the user models::

    python manage.py migrate user
    python manage.py migrate svn
    python manage.py migrate

7. Prepare frontend static file(directory is dist/)::

    mkdir -p $python_site_packages/svnlab/frontend/dist
    cp -rf dist/* $python_site_packages/svnlab/frontend/dist

8. Run svnlab::

    python3.7 manage.py runserver 0.0.0.0:8888

9. Start use or develop svnlab.

Quick Develop
-------------

1. Add "user" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'user',
    ]

2. Include the user URLconf in your project urls.py like this::

    path('user/', include('user.urls')),

3. Run `python manage.py makemigrations` to create the user migrations.

4. Run `python manage.py migrate` to create the user models.

5. Add frontend static file to svnlab/frontend/dist. And start the development 
   server that run `python manage.py runserver 127.0.0.1:8000`.

6. Visit http://127.0.0.1:8000/ to participate in the user.
