# hola
Quản lý chi tiêu

# Setup

## Init project
1. Create local config file
```
$ cp config.py.example config.py
```

2. Create virtual environment
```
$ python3 -m venv env
$ souce env/bin/activate # Enter virtualenv
```

3. Install dependencies
```
$ pip install -e .
```

## For development
```
$ source FLASK_APP=api
$ flask run
```

## For production
Use uWSGI for web server with Nginx proxy
```
$ env/bin/uwsgi --socket 0.0.0.0:5000 --protocol http wsgi:hola_api
```