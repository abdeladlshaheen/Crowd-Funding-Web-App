# Crowd-Funding-Web-App

### Installation

1. git clone https://github.com/abdeladlshaheen/Crowd-Funding-Web-App.git
2. python3 -m venv .venv
3. source .venv/bin/activate
4. python3 -m pip install django
5. cd Crowd-Funding-Web-App/
6. pip install -r requirements.txt
7. python3 manage.py runserver

<hr/>

After installing packages, please go to the root directory of the project and type this command on your terminal (make sure that requirements.txt is in the root directory).
   - pip freeze > requirements.txt

### Upgrade Packages

Inside Crowd-Funding-Web-App directory, make sure that requirements.txt exists

1. pip install pip-upgrader
2. pip-upgrade

### After you pull from github

1. go to settings.py to change database configurations to suit your local database
2. check "Installing packages from requirements.txt" section
