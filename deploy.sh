#!/usr/bin/env bash

SCRIPT_FILE=$0
APP_PATH=$(dirname $SCRIPT_FILE)
cd $APP_PATH

git reset HEAD || exit 1
git checkout .
git pull origin main

if [ ! -d "${PWD}/env" ]; then
    python3 -m venv env || exit 1
fi

eval './env/bin/pip install -e .' || exit 1

sudo supervisorctl restart hola_api
