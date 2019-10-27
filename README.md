# passwdservice
This service is written in django and uses the django-rest-framework for creating REST APIs

## Setup Instructions

### Clone the repository
```
git clone https://github.com/sujjunair/passwdservice.git
```

### Setup Docker

#### Install Docker
Install Docker for Mac from here: https://docs.docker.com/docker-for-mac/install/

### Bring up Containers
#### Start Containers
```
docker-compose up -d
```

To access your local server, go to http://127.0.0.1:8000

All endpoints are available as browsable APIs, so you can test endpoints using the browser.
For instance to see list of users, go to http://127.0.0.1:8000/users

#### List Containers
To list containers, use
```
docker-compose ls
```


## Run tests
```
docker-compose exec webapp python manage.py test
```

## Modify passwd and grp file paths
Go to settings.py and change ```PASSWD_FILEPATH``` and ```GRP_FILEPATH```
Defaults are as follows:
```
PASSWD_FILEPATH = '/etc/passwd'
GRP_FILEPATH = '/etc/group'
```
You might have to restart the local server after modifying these values.
