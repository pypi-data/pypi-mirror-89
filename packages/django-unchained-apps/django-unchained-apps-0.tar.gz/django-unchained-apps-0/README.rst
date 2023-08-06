=====================
Django unchained apps
=====================
This is a package that contains many of unchained apps:
- unchained_auth
- unchained_chat
- unchained_notification

Quick start
-----------

1. Install the lib: 

     pip install django-unchained-apps


1. Add "foo" to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = [
        ...
        'unchained_auth',
        'unchained_chat',
        'unchained_notification'
        ...
    ]

2. Include the foo URLconf in your project ``urls.py`` like this::

    path('', include('un_foo.urls')),

3. Add this variable ``FOO_SETTING`` to ``settings.py``


4. You will find the foo api documentation in  `/foo/`.

