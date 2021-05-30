# Industrial Training Course Server
Server side application to control devices through 4G / 5G network. Part of Aalto University ELEC-C7430 Industrial Training course.

## Configure
```
$ export FLASK_APP=flaskr
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
$ mkdir instance
$ touch instance/config.py
```

In config.py:
```
ADMIN_PASS = "some-password"
SECRET_KEY = b'some-random-string'
```
here ADMIN_PASS is required for registering new users. SECRET_KEY is required by Flask application.

Then, initialize the sqlite database:
```
$ flask init-db
```

## Deployment

### With Docker
```
$ docker build -t indtrain .
$ docker run -d -p 5050:5050 indtrain
```
### Manually
```
$ pip install waitress
$ waitress-serve --port=5050 --call flaskr:create_app
```