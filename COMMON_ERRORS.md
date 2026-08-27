# Common Terminal Errors and Solutions

## Error: Access Denied for MySQL Root User

### When This Happens

This error occurs when MySQL rejects the username, password, or authentication method being used.

Common causes include:

- The MySQL password does not match the password configured in `testing.yml` or `default.yml`.
- The MySQL user is using a different authentication plugin than expected.
- MySQL was recently installed or reconfigured.
- The local database credentials are not configured correctly.

### Terminal Output

```bash
ERROR 1045 (28000): Access denied for user 'root'@'localhost'
```
### Possible Solutions

Update the MySQL `root` account so it can authenticate on `localhost` using the password expected by the application:

```bash
sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'root'; FLUSH PRIVILEGES;"
```

This sets the `root@localhost` password to `root` and uses the `caching_sha2_password` authentication method. The password should match the password configured for your local database setup.

Also make sure the database configuration points to the local MySQL server and uses the correct credentials:

```yml
db:
    name: "celts"
    host: "localhost" # use localhost instead of db for a local MySQL server
    username: "celts_user"
    password: "root" # use the password configured for this MySQL user 
```

## Error: pem: command not found

### When This Happens

This error occurs when the `peewee-migrations` package is installed, but the `pem` executable is not available in the terminal's `PATH`.

This commonly happens on macOS when `pip` installs the package into the user's Python directory, such as:

```~/Library/Python/3.12/bin ```

### Terminal Output

```bash
zsh: command not found: pem
```

You may also see that the package is already installed: ```Requirement already satisfied: peewee-migrations```

but running: ```pem --help```; still returns ```zsh: command not found: pem```

### Possible Solution

First, locate the Python user installation directory: ```python3 -m site --user-base```

Then add its bin directory to your PATH.

For example: ```export PATH="$PATH:$HOME/Library/Python/3.12/bin"```

To make the change permanent, open your Zsh configuration file: ```nano ~/.zshrc```

Add: ```export PATH="$PATH:$HOME/Library/Python/3.12/bin"```

Reload the terminal configuration: ```source ~/.zshrc```

Then verify that pem is available: ```pem --help```

Afterward, Peewee migration commands should work.

Note: Make sure peewee-migrations is installed in the same Python environment being used by the project.

## Error: `venv/bin/activate: No such file or directory` and `externally-managed-environment`

### When This Happens

This occurs when `setup.sh` tries to activate a Python virtual environment that does not exist or was not created correctly.

Because the virtual environment is missing, the following `pip` commands run against the system Python instead. On newer Ubuntu versions, system Python is protected by PEP 668, which causes the `externally-managed-environment` error.

### Terminal Output

```bash
bash: venv/bin/activate: No such file or directory
```

Followed By:

```
error: externally-managed-environment

× This environment is externally managed
```

### Possible Solution
Make sure the Python virtual environment package is installed:

sudo apt update
sudo apt install python3.14-venv