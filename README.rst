===============
Django Sprinter
===============

Django Sprinter is a tool that brings more fun to Django Sprints. Each 
registered sprint participant - if her Trac or GitHub login is provided - 
will stand a chance to unlock some sprint achievements. 

Project layout
==============

{{ project_name }}/settings/
    contains project settings for production and development

requirements/
    contains project requirements for production and deveopment

templates/
    project wide templates (404 and 500 included)

static/
    for storing project-wide static files

public/
    default destination for ``collectstatic``


``manage.py`` and ``wsgi.py``
=============================

Both files have disabled default settings file detection.
This is to protect you from launching your app with wrong
settings file. If you know what you are doing, uncomment
interesting lines in those files.

