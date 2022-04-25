# Crowd-Funding-Web-App

### Installation

1. To run the project:
   - git clone https://github.com/abdeladlshaheen/Crowd-Funding-Web-App.git
   - python3 -m venv .venv
   - source .venv/bin/activate
   - python3 -m pip install django
   - python3 Crowd-Funding-Web-App/manage.py runserver
2. To configure your database:
   - pip install mysqlclient
3. To set up API:
   - pip install djangorestframework
     <br/><br/>

- python -m pip install Pillow
- pip install django-countries
<hr/>

4. after installing packages, please go to the root directory of the project and type this command on your terminal.
   - pip freeze > requirements.txt
     make sure that requirements.txt is in the root directory

### Installing packages from requirements.txt
1. make sure you are in requirements.txt path
2. pip install -r requirements.txt

### Upgrade Packages

Inside Crowd-Funding-Web-App directory, make sure that requirements.txt exists

1. pip install pip-upgrader
2. pip-upgrade

### After you pull from github
1. go to settings.py to change database configurations to suit your local database
2. check "Installing packages from requirements.txt" section