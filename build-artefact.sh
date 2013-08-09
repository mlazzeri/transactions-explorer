#!/bin/bash -e

mkdir -p artefacts
rm -f artefacts/*

VIRTUALENV_DIR=/var/tmp/virtualenvs/$(echo ${JOB_NAME} | tr ' ' '-')
export PIP_DOWNLOAD_CACHE=/var/tmp/pip_download_cache

virtualenv --clear --no-site-packages $VIRTUALENV_DIR
source $VIRTUALENV_DIR/bin/activate

pip install -r requirements.txt

python fetch_csv.py --client-secrets /etc/google/oauth/client_secrets.json --oauth-tokens /var/lib/google/oauth/drive.db
python create_pages.py

cd output
tar -zcvf ../artefacts/service-explorer.tgz .
