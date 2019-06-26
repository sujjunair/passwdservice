# passwdservice
This service is written in django and uses the django-rest-framework for creating REST APIs

## Setup Instructions

### Clone the repository
```
git clone https://github.com/sujjunair/passwdservice.git
```

### Setup python3 and virtual environment

#### Install Python3
Install python3 from here: https://www.python.org/downloads/ 

#### Setup virtual env and install dependencies
```
cd passwdservice
virtualenv -p python3 py3env
pip install -r requirements.txt
```

### Start Local Server
```
cd passwd
python manage.py runserver
```
To access your local server, go to http://127.0.0.1:8000

All endpoints are available as browsable APIs, so you can test endpoints using the browser.
For instance to see list of users, go to http://127.0.0.1:8000/users

## Run tests
```
python manage.py test
```

## Modify passwd and grp file paths
Go to settings.py and change ```PASSWD_FILEPATH``` and ```GRP_FILEPATH```
You might have to restart the local server after modifying these values.
