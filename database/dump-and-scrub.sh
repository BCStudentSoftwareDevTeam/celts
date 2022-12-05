#!/bin/bash

########################################################
# Dump the production database and scrub sensitive data
########################################################

# Get credentials
echo -n "Database/Schema Name: "
read DB

echo -n "Application User: "
read USER

echo -n "Application Password: "
read -s PASS
echo

CONN="-u $USER"
TMPDB="dumptmp"

export MYSQL_PWD="$PASS"

# Dump application schema into another database
echo -n -e "\nCreate temporary database ... "
mysql $CONN -e "CREATE DATABASE IF NOT EXISTS \`$TMPDB\`"
mysqldump $CONN $DB | mysql $CONN $TMPDB
echo -e "done.\n"

# Execute SQL in data-scrub.sql
# watch out for those escaped quotes if you have to change something
awk "
    /--/ {print}
    /^[^-]/ {
        printf \"EXECUTING: %s\n\n\",\$0
        system(\"mysql $CONN $TMPDB -e \\\" \" \$0 \" \\\" \")
    }
" data-scrub.sql

# Dump scrubbed data to prod-backup.sql
echo -n -e "\nDump scrubbed data to prod-backup.sql ... "
mysqldump $CONN $TMPDB > prod-backup.sql
echo -e "done.\n"

# Remove temporary database
mysql $CONN -e "DROP DATABASE \`$TMPDB\`"

# Reset password
export MYSQL_PWD=

# Don't do the git actions automatically
echo "git add prod-backup.sql"
echo "git commit -m 'Add an up to date production backup'"
