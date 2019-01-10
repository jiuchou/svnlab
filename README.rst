======
SvnLab
======

SvnLab is a simple Django app to manage svn server. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

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