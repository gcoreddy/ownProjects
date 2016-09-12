#1: Project Creation
====================
"sqa" folder corresponds to the "sqa" PROJECT.
Django Command used: django-admin startproject sqa .

#2: Database Setup
==================
Default sqllite3 is used.
Django Command Used: (From dir where manage.py is present): python manage.py migrate

#3: Application Creation
=========================
"sqadasboard" folder corresponds to the "sqadashboard" APPLICATION.
Django Command Used: (From dir where manage.py is present): python manage.py startapp sqadashboard 

#4: Starting the Web Server
===========================
Django Command Used: (From dir where manage.py is present): python manage.py runserver