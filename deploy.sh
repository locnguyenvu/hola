#!/usr/bin/env bash

if [ -z $PROJECT_DIR ]; then
    echo 'Project directory not found!!!'
    exit 1
fi

cd $PROJECT_DIR || exit 1

git reset HEAD || exit 1
git checkout .
git pull origin main

if [ ! -d './env' ]; then
    python3 -m venv env || exit 1
fi

eval './env/bin/pip install -e .' || exit 1

sudo supervisorctl restart hola_api
