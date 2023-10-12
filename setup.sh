#!/usr/bin/env bash

# Check for correct python version
VERSION=`python3 --version | awk '{print $2}'`
if [ "${VERSION:0:1}" -ne "3" ] || [ "${VERSION:2:1}" -lt "7" ] || [ "${VERSION:2:1}" -gt "9" ]; then
	echo "You must use Python 3.7 - 3.9. You are using $VERSION"
    echo "When upgrading, remember to install python3.X-dev and python3.X-venv (and maybe the right pip)"
	#return 1
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
if [[ ! -e app/config/local-override.yml ]]; then
	echo "Remember to edit your specific mail settings and Tracy connection information in 'app/config/local-override.yaml'"
	echo "# Add sensitive information to this file and do not commit to version control
tracy:
  password: replace
  
MAIL_USERNAME: 'gmail address'
MAIL_PASSWORD: 'app password'" > app/config/local-override.yml
	echo
	echo "If your database has not been set up, you will need to run database/reset_database.sh"
fi

export FLASK_DEBUG=1
export FLASK_APP=run.py
export APP_ENV=development
export FLASK_RUN_PORT=8080
export FLASK_RUN_HOST=0.0.0.0   # To allow external routing to the application for development
