After git cloning the project into a local folder, please follow these steps:

## 1. Install python and pip locally.

### python ###

Use the most recent version available <a href="https://www.python.org/downloads/">here</a>.

The project currently uses Python version 3.9.2.

### pip ###

To check if pip is installed, run:
```
python -m pip --version
```

If not installed, run the following commands to install:
```
C:\> curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
C:\> python get-pip.py
```

## 2. Install pipenv

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world.

To check if pipenv is installed, run:
```
pipenv check
```

If not installed, run the following command to install:
```
pip install pipenv
```

For Linux, it is important to check if the current bash has a path to `~/.local/bin`.

## 3. Run project using virtual environment (venv)

Inside the project's folder, run the following command:
```
mkdir .venv
```

Now, inside the project's folder, run the following command:
```
pipenv shell
```

This command spawns a shell within the virtualenv.

All `python` and `pip` commands will be executed using the binaries created by the virtual enviroment.

Type 'exit' or 'Ctrl+D' to return.

## 4. Install the project dependencies

This command should be executed within the virtual environment.
Execute the `pipenv shell` before installing the packages:

Inside the project's folder, run the following command:
```
pipenv install
pipenv install --dev
```

All dependencies found inside `Pipfile` will be installed.

## 5. Build the project

Run command:
```
pyinstaller formula-graham.py --onefile
```

## 6. Run the project

Run command:
```
python formula-graham.py
```

## 7. Exit the virtual environment:

Run command:
```
exit
```
