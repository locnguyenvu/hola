#!/bin/bash

PROJECT_DIR=$(git rev-parse --show-toplevel)
VENV_PIP="$PROJECT_DIR/env/bin/pip"
VENV_PYTHON="$PROJECT_DIR/env/bin/python"

git reset HEAD
git checkout .
git pull origin main

eval "$VENV_PIP"' install -e .'

sudo supervisorctl restart hola_api
