# Common Terminal Errors and Solutions

<details>
<summary>Error: Access Denied for MySQL Root User</summary>

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
</details>

<details>
<summary>Error: pem: command not found</summary>

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

</details>

<details>
<summary>Error: `venv/bin/activate: No such file or directory` and `externally-managed-environment`</summary>

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

```
sudo apt update
sudo apt install python3.14-venv
```

Create the virtual environment manually: ```python3 -m venv venv```

Verify that it was created: ```ls venv```

You should see directories such as:

```bash
bin  include  lib  lib64  pyvenv.cfg
```

Activate the environment: ```source venv/bin/activate```

Then run the setup script again: ```source setup.sh```

Once the virtual environment is active, pip installs packages inside venv instead of attempting to modify the system Python installation.

Note: Avoid using --break-system-packages for this project. The dependencies should be installed inside the project's virtual environment.
</details>

<details>
<summary>Error: `(venv)` Is Active but `externally-managed-environment` Still Appears</summary>
</details>

<details>
<summary>Error: Virtual Environment Fails Inside `/mnt/c/...` on WSL</summary>
</details>

<details>
<summary>Error: Forgot MySQL Root Password / `Access denied for user 'root'@'localhost'`</summary>
</details>

<details>
<summary>Error: Collecting a requirement from `requirements.txt` fails because of Python version incompatibility</summary>

## Error: Dependency Installation Fails Due to Python Version Mismatch

### When This Happens

This error can occur when running: ```pip install -r requirements.txt``` or when running a project setup script that installs packages from `requirements.txt` like source setup.sh. 

Some packages only support certain Python versions. If the Python version used by the virtual environment is too new, too old, or otherwise incompatible with a dependency, `pip` may fail while collecting, building, or installing that package.

Common causes include:

- The virtual environment was created with a Python version that is not supported by one or more project dependencies.
- A package in `requirements.txt` is pinned to an older version.
- The local Python version is different from the version the project was originally developed or tested with.
- A dependency relies on Python functionality that was removed or changed in newer Python versions.

For CELTS, make sure you are using a supported Python version. The minimum required Python version is Python 3.10+.

### Example Terminal Output

One example is `pathtools==0.1.2` failing under Python 3.12:

```bash
Collecting pathtools==0.1.2 (from -r requirements.txt (line 44))
Using cached pathtools-0.1.2.tar.gz
Installing build dependencies ... done
Getting requirements to build wheel ... error

ModuleNotFoundError: No module named 'imp'

ERROR: Failed to build 'pathtools' when getting requirements to build wheel
```

The exact error may differ depending on the package.

Look for output similar to: ```Collecting <package-name>```

followed by an error related to building, installing, or Python compatibility.

### Possible Solution

First, check which Python version is currently being used: ``` python --version ```

You can also check: ``` python3 --version ```

If the current Python version is incompatible with the project's dependencies, create the virtual environment using another supported Python version.
For example, Python 3.11 may be used when a dependency does not support Python 3.12.

First, deactivate and remove the existing virtual environment:

```bash
deactivate
rm -rf venv
```

### Installing Another Python Version on macOS

- On macOS with Homebrew, you can install a specific Python version with: ```brew install python@3.11```
- Verify that it is installed: ```python3.11 --version```
- Then create the virtual environment using that Python version: ```python3.11 -m venv venv```

### Installing Another Python Version on Linux

- First update your package list: ```bash sudo apt update ```
- Then install Python 3.11 and the virtual environment package: ```bash sudo apt install python3.11 python3.11-venv ```
- Verify the installation: ```bash python3.11 --version ```

### Finding a Specific Python Installation

If the Python version you want is already installed but a command such as `python3.11` does not work, locate the Python executable first.

Check the default Python location: ``` which python3 ```

Check for a specific version: ``` which python3.11 ```

#### With MacOS

You can also look for installed Python executables.
- On Apple Silicon Macs: ``` ls /opt/homebrew/bin/python* ```
- On Intel Macs: ``` ls /usr/local/bin/python* ```

#### With Linux

- On Linux, Python executables are commonly located in `/usr/bin` or `/usr/local/bin`. 
- Check `/usr/bin`: ```bash ls /usr/bin/python* ``` 
- Check `/usr/local/bin`: ```bash ls /usr/local/bin/python* ```

If you find the Python executable at a specific path, use that path directly when creating the virtual environment.

For example: ```/opt/homebrew/bin/python3.11 -m venv venv``` or ``` /usr/local/bin/python3.11 -m venv venv ```

The general format is: ``` /path/to/python -m venv venv ```

### Activate and Verify the Virtual Environment

- Activate the new virtual environment: ``` source venv/bin/activate ```
- Verify the Python version: ``` python --version ```
- Also verify which Python executable the virtual environment is using: ``` which python ```
- It should point to the Python executable inside the project's virtual environment, similar to: ``` /path/to/project/venv/bin/python ```

### Retry the Installation

Once the virtual environment is using a compatible Python version, retry the dependency installation:

```bash
source setup.sh
```

### Key Takeaway

If installation fails while collecting or building a package from `requirements.txt`, check the Python version before assuming the dependency itself is missing.

The `pathtools` error above is one example, but similar installation errors can occur with other packages when the Python version is incompatible with the project's dependencies.

</details>
