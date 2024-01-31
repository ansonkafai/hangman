# Technical Test - Hangman Game

## Prerequisites

Before running the app,
please check if your local machine meets the following requirements:

1. Python 3.8 or later is installed. [Download Python](https://www.python.org/downloads/release/python-3814/)
1. The below paths are added to the system path:
   ```shell script
   <Python installation root>/
   <Python installation root>/Scripts/
   ```

## Steps for running the game on Windows

Assume the project is cloned to your local path `C:\tmp\hangman\`.

1. Open a Windows command prompt and run the below commands to create venv:
    ```commandline
    cd C:\tmp\hangman
    python -m venv venv
    cd venv/Scripts
    activate.bat
    pip install -U pip
    cd C:\tmp\hangman
    pip install -r requirements.txt
    ```

1. Run the below command to execute linting and unit testing:
    ```commandline
    tox
    ```

1. Run the below command to start the game:
    ```commandline
    python -m hangman
    ```

    <img src="./hangman.jpg" width="100%" height="100%">

## Steps for running the game on Linux

Assume the project is cloned to your local path `/tmp/hangman`.

1. Open a terminal session and run the below commands to create venv:
   ```shell script
   cd /tmp/hangman
   python -m venv venv
   source venv/Scripts/activate
   pip install -U pip
   pip install -r requirements.txt
   ```

1. Run this command to execute linting and unit testing:
   ```shell script
   tox
   ```

1. Run this command to start the game:
    ```shell script
    python -m hangman
    ```
    
## Tech Stack

| Framework                                            | Version     |
|------------------------------------------------------|-------------|
| [Click](https://click.palletsprojects.com/en/8.1.x/) | 8.1.3       |
| [pytest](https://docs.pytest.org/)                   | 7.4.3       |
| [tox](https://tox.wiki/)                             | 3.27.1      |
