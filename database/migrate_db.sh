
pem init

# See: https://stackoverflow.com/questions/394230/how-to-detect-the-os-from-a-bash-script/18434831
if [[ "$OSTYPE" == "linux-gnu" ]]; then
        # Linux
    sed -i 's/migrations/lsf_migrations/g' migrations.json
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
    sed -i '' 's/migrations/lsf_migrations/g' migrations.json
fi

#pem add app.models.[filename].[classname]
pem add app.models.course.Course
pem watch
#pem migrate
