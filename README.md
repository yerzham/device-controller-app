# Industrial Training Course Server
Server side application to control devices through 4G / 5G network. Part of Aalto University ELEC-C7430 Industrial Training course.

## Configure
Create a config.py in the instance folder:

```
$ mkdir instance
$ touch instance/config.py
```

In config.py:
```
ADMIN_PASS = "some-password"
SECRET_KEY = b'some-random-string'
```
here ADMIN_PASS is required for registering new users. SECRET_KEY is required by Flask application.

## Deployment and maintenance (Docker or manually)

### With Docker
With Docker, web application can keep working in the background and it will also automatically restart after a server reboot.
Docker has more potential in terms of deployment automation but it was not fully used here.
#### Deployment
Create a docker volume to store a database file:
```
$ docker volume create indtrain-db
```
Build the image and run the container:
```
$ docker build -t indtrain .
$ docker run -d -p 5050:5050 --name indtrain --restart always -v indtrain-db:/tmp indtrain
```
#### Features
Stop or start the web application:
```
$ docker stop indtrain
$ docker start indtrain
```
Delete the build:
```
$ docker rm indtrain
$ docker rmi indtrain
```
Reset the database:
```
$ docker stop indtrain
$ docker rm indtrain
$ docker volume rm indtrain-db
$ docker volume create indtrain-db
$ docker run -d -p 5050:5050 --name indtrain --restart always -v indtrain-db:/tmp indtrain
```
Update the build (Database persists):
```
$ docker stop indtrain
$ docker rm indtrain
$ docker rmi indtrain
$ git pull
$ docker build -t indtrain .
$ docker run -d -p 5050:5050 --name indtrain --restart always -v indtrain-db:/tmp indtrain
```
### Manually
#### Deployment
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install waitress
$ pip install -r requirements.txt
$ waitress-serve --port=5050 --call flaskr:create_app
```
#### Features
Reset the database:
```
rm /tmp/flaskr.sqlite
```
Update the build (Database persists):
```
$ git pull
```
