#!/bin/bash

PRODUCTION=0
if [ "`hostname`" == 'CS-CELTS' ]; then
	echo "DO NOT RUN THIS SCRIPT ON PRODUCTION UNLESS YOU REALLY REALLY KNOW WHAT YOU ARE DOING"
	PRODUCTION=1
	exit 1;
fi

cd database/

########### Fetch Prod Data ############
PRIVATE_DATA_REPO="git@github.com:BCStudentSoftwareDevTeam/prod-data.git"
DATA_DEST_DIR="prod-data"
APP="celts"
BACKUP_FILE="$DATA_DEST_DIR/$APP/prod-backup.sql"

fetch_backup() {
    if [ -d "$DATA_DEST_DIR/.git" ]; then
        git -C "$DATA_DEST_DIR" fetch --quiet --depth 1 origin main &&
        git -C "$DATA_DEST_DIR" reset --quiet --hard FETCH_HEAD
    else
        git clone --quiet --depth 1 --filter=blob:none --sparse "$PRIVATE_DATA_REPO" "$DATA_DEST_DIR" &&
        git -C "$DATA_DEST_DIR" sparse-checkout set "$APP"
    fi
}

########### Process Arguments ############
BACKUP=0
BASE=0
TEST=1
if [ "$1" == "from-backup" ]; then
	BACKUP=1
	TEST=0
elif [ "$1" == "base" ]; then
	BASE=1
	TEST=0
elif [ "$1" == "test" ]; then
	:
else
    echo "You must specify which data set you want to restore"
    echo "Usage: ./reset_database.sh [from-backup|base|test]"
    exit;
fi

########### Recreate Database Schema ###########
echo "Dropping databases"
mysql -u root -proot --execute="DROP DATABASE \`celts\`; DROP USER 'celts_user';"

echo "Recreating databases and users"
mysql -u root -proot --execute="CREATE DATABASE IF NOT EXISTS \`celts\`; CREATE USER IF NOT EXISTS 'celts_user'@'%' IDENTIFIED BY 'password'; GRANT ALL PRIVILEGES ON *.* TO 'celts_user'@'%';"


# remove ahead of time in case we didn't clean up last time
rm -rf migrations
rm -rf migrations.json

if [ $BACKUP -eq 1 ]; then
    echo "Retrieving latest backup"

    if ! fetch_backup 2>/dev/null; then
        if [ -f "$BACKUP_FILE" ]; then
            echo "Warning: couldn't update backup from private repo; using existing local copy."
        else
            echo "Warning: couldn't access $PRIVATE_DATA_REPO (do you have access?)."
            echo "Falling back to an empty database."
            BACKUP=0
        fi
    fi
fi

echo -n "Creating database objects"
if [ $BACKUP -eq 1 ]; then
    echo " from backup"
    mysql -u root -proot celts < $BACKUP_FILE

    echo "Running in-progress.sql"
    mysql -u root -proot celts < in-progress.sql
else
    echo " empty"
    ./migrate_db.sh no-backup
fi

# remove so we do a fresh migration next time
if [ $PRODUCTION -ne 1 ]; then
    rm -rf migrations
    rm -rf migrations.json
fi


############ Add Data (if needed) ##############

# Adding data we need in all environments, unless we are restoring from backup
if [ $BACKUP -ne 1 ]; then
    python3 base_data.py
else
    echo "You have imported the production DB backup."
fi

# Adding fake data for non-prod, set up admins for prod
if [ $PRODUCTION -eq 1 ]; then
	APP_ENV=production python3 import_users.py
	APP_ENV=production python3 add_admins.py
elif [ $BACKUP -ne 1 ]; then
    if [ $TEST -eq 1 ]; then
	    python3 test_data.py
    fi
fi

# NOW we can re-run our tests
touch ../setup.sh
