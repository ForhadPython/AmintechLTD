( First you need to create a virtual environment ) 
1 | pip install virtualenv
2 | virtualenv env
( Then you have to make an entry in the environment ) 
( Then you need to install the requisition files )
3 | pip install Django==3.0
4 | pip install Pillow
5 | pip install django-import-export
6 | pip install django-ckeditor
7 | python manage.py migrate
8 | python manage.py makemigrations
9 | python manage.py migrate
   ( Then you need to create a superuser )
10 | python manage.py createsuperuser 
11| Username : xyz
12 | Password : xtz
13| confirm Password :: xyz
14 | python manage.py makemigrations
15 | python manage.py migrate
