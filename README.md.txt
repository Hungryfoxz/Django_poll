###########################################
       Project Name : balot
##########################################
date : 29.05.2022
*Start with creating an stanalone environment for the project..
$py -m venv <name_of_environment>
$py -m pip install django
$django-admin startproject <project_name>
$ cd <project_name>
$ django-admin startapp <app_name>
$ py mange.py createsuperuser    =>Username : admin, Passwd : admin
   added normal user    => Username : precidingofficer, Password: notanadmin@123
##########################################
FIle Structure >>
	--ballot
	   |________ settings.py
	   |________ urls.py
	   |________ wsgi.py
	   |________ asgi.py
	   |_______ __init__.py
	--PO
	   |________ migrations	  
	   |________ __init__.py
	   |________ admin.py
	   |________ apps.py
	   |________ models.py
	   |________ urls.py
	   |________ views.py
	   |________ tests.py
	--static
	--templates
	   |________ base.html
	   |________ index.html
	   |________ login.html
	   |________ povo_home.html
	   |________ preciding_officer.html
	   |________ voter.html
	   |________ voter_show_ballot.html
	--db
	--manage
#############################################