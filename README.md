# Flask application to manage CELTS programs

## Requirements
 * Python 3.7+

**Packages (Ubuntu)**
 * python3-dev
 * python3-pip
 * python3-venv
 * libffi-dev
 * mysql-server


**Assumptions**
 * Mac OS or Linux
 * mysql ```root``` user is accessible by a non-root OS user, with password ```root``` (in order to run ```reset_database.sh```
 * default python is Python 3

## Developing on CELTS
1. Pull down the repo in your home directory: ```git clone <URL>```
2. Run ```source setup.sh```
3. Ensure mysql is running. You may need to do ```sudo systemctl start mysql``` or ```/etc/init.d/mysql start``` (Linux) or ```brew services start mysql``` (Mac OS with Homebrew)
4. If you have non-default root and application database credentials, match your MySQL configuration to the application config. You can either:
    - Update MySQL to use the database, username, and password in ```app/config/default.yml```. *OR*
    - Copy the ```db``` configuration lines from ```app/config/default.yml``` and paste them into ```app/config/local-override.yml```. Edit them to create custom database, username, and password configurations. They will need to match what is in your MySQL service.  
5. In the database directory, run ```./reset_database.sh test```. Use ```real``` instead of ```test``` to use production data.
6. Run the app with ```flask run``` in the root directory

## Testing
Tests should be added in `tests/code/`, logically grouped into files named `test_EXAMPLE.py`. You can run tests individually with `pytest`, or run the entire suite with `tests/run_tests.sh` or `tests/monitor.sh`. `tests/run_tests.sh` will only execute the test suite once, where `tests/monitor.sh` will rerun the test suite everytime a change is made and saved. In most cases, `tests/monitor.sh` should be used over `tests/run_tests.sh`. Where possible, use TDD (Test-Driven Development) and write your test before the code that makes it pass. Follow the Fail - Implement - Pass cycle.

When running tests, an optional parameter is available. If you would like to run tests in more detail and see which tests specifically pass and fail run `tests/monitor.sh --verbose`. To test once specific file instead of the whole suite, add the path to the file after a run tests command like so: `tests/monitor.sh tests/code/test_sampleFile.py`. 

## Pull Requests

### General Pull Request Checklist
1. The code fixes the issue the author is saying it fixes. 
2. The code is well designed.
3. There is no existing code that serves the same functionality. 
4. The code is adequately tested. 
5. Variable, Class, and Method names are purposeful.
6. Code is well commented and functions include docstrings.
7. Update the documentation if relevant.
8. SSDT coding practices are followed. 

### GitHub Actions
GitHub Actions is a continuous integration/delivery tool we use that allows us to automatically test our code on push. When you prepare to merge a branch into development, GitHub Actions will run our test suite on Python versions 3.7-3.11 and prevent you from merging your code into development if there are any failing tests. You can see the status of the test suite with an icon next to the pull request title that will display a check if all the tests are passing or an x if the tests are failing. GitHub actions will give you a more in depth breakdown of the tests if you are viewing a specific pull request.

If you would like to learn more about Actions you can read more here: https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions

## Troubleshooting
1. If you can't clone the repository, make sure your SSH public key is added to your GitHub profile.
2. Make sure that you are running `source setup.sh` and `./reset\_database.sh`, in that order, without errors. Errors there should be resolved first.

## Other Tasks

### Accessing the Logged-in user
The currently logged-in user is stored in Flask's request global variable `g`. Import it with `from flask import g`, and then you can access the user data in your controller with `g.current_user`. Jinja templates can also access this variable without an import, with `{{g.current_user}}`.

The default user is set in defaults.yml. If you want to change the user for testing purposes, add a `default_user` item in `config/local-override.yml`. The user will be loaded from the database, or created if none exists. Since there is no Active Directory data in development, if you want the data to be correct you should add the user to `database/test_data.py`.

### Resetting Database
1. Run ```reset_database.sh``` to rebuild your database. If you want to preserve your data, run ```migrate_db.sh```or do it manually (see below).

### Updating pip dependencies (imports)
1. Run ```pip freeze > requirements.txt``` to export all imports to a file. This file is used by **setup.sh** when the next user runs ```source setup.sh```

### Updating Models Manually
Use Peewee Migrator to update models: https://pypi.org/project/peewee-migrations/. Usually in development you will just reset your database to get it back in a 'clean' state.

1. Install: ```pip install peewee-migrations``` (included in setup.sh, so you shouldn't need this)
2. ```pem init```
3. Add models to watch: e.g., ```pem add app.models.user.User```
4. Watch the model for changes: ```pem watch```
5. When done changing models, run the migrator to modify the db: ```pem migrate```

NOTE: You don't need to watch the files before you begin making changes.
The watch will compare the db to your model file and make any changes that are inconsistent.

Additional helpful commands:
List active migrations: ```pem list```
Show SQL generated by changes to the model: ```pem show```

If encountering issues, run ```reset_database.sh```.

### Email Configuration
There are a couple of options to test email handling. By default, all emails will be logged to the slack channel #celts-emails in the bereacs workspace.

If you want to test with actual emails, use an email other than outlook to test email handler. This setup is specific to gmail, but should work with any other email that allows you to make app passwords

1. Set up two factor authentication on your Gmail (Security Settings)
2. Create an App Password through your Gmail. This 16 character password can only be viewed once, so make sure to save it. (NOTE: You won't have the option to create an app password unless step one is completed)
3. Inside of your secret_config.yaml file set the MAIL_USERNAME and MAIL_DEFAULT_SENDER as your Gmail, set the MAIL_PASSWORD as your new app password as, and set ALWAYS_SEND_MAIL as True. If you want emails to go to their real recipients, remove MAIL_OVERRIDE_ALL from your config or set it to "".
4. For testing purposes, change the email of the student and supervisor to match another email that can receive your test emails (or you can use MAIL_OVERRIDE_ALL to send everything to the address specified.
