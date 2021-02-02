#!/usr/bin/env bash

# Check for correct python version
VERSION=`python3 --version | awk '{print $2}'`
if [ "${VERSION:0:1}" -ne "3" ] || [ "${VERSION:2:1}" -lt "6" ] || [ "${VERSION:2:1}" -gt "8" ]; then
	echo "You must use Python 3.6 - 3.8. You are using $VERSION"
	echo "When upgrading, remember to install python3.X-dev and python3.X-venv"
	return 1
else
	echo -e "You are using Python $VERSION"
fi

# Create a virtual environment for dependencies
if [ ! -d venv ]
then
  python3 -m venv venv
fi
. venv/bin/activate

# upgrade pip
python3 -m pip install --upgrade pip #added python-m for pip installs (source setup overwrite for venv)

# install requirements
python3 -m pip install -r requirements.txt
# To generate a new requirements.txt file, run "pip freeze > requirements.txt"

echo
if [[ ! -e app/config/secret_config.yaml ]]; then
	cp app/config/example_secret_config.yaml app/config/secret_config.yaml
	echo "Remember to edit your mail settings and MySQL connection information in 'app/config/secret_config.yaml'"
	echo
	echo "If your database has not been set up, you will need to run database/reset_database.sh"
fi

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=8080
