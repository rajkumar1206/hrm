# Colors HR Management Backend sytem

Colors recently added an Entity Relatioship Diagram which is designed on StarUML application. 

## Steps to user downloding or cloning...

create and enter the dir which u need to use

1. git init
2. git remote add origin https://github.com/KavachNetworks/Colors_HRMS_BE.git
3. git pull origin master
4. pip install virtualenv
5. virtualenv env
6. env/Sripts/activate
7. pip install -r requirements.txt
8. pip install django-rest-auth[with_social]
9. cd colors
10. python manage.py makemigrations
11. python manage.py migrate --syncdb
12. python manage.py createsuperuser
13. python manage.py runserver

### If there is any update in your code and if u need to reflect in editor

1. git pull origin master

### if u have update your code.. and want to update in github

1. git add .
2. git commit -m "add the descp"
3. git push origin master


### URL Endpoints....

* login : https://localhost:8000/rest-auth/login/
* logout : https://localhost:8000/rest-auth/logout/
* register : https://localhost:8000/rest-auth/registration/ 
* employee list : https://localhost:8000/employee/list/ 
* employee details : https://localhost:8000/employee/:employee_id/
* Delete employee : https://localhost:8000/employee/:employee_id/delete/
* Update employee : https://localhost:8000/employee/:employee_id/update/
* Add employee : https://localhost:8000/employee/create/
