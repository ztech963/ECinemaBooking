

## Here's the environment variables to set
export FLASK_APP=ecinema
export FLASK_ENV=development

## To run:
- install Python3.7 and Flask
- run pip3 install -e . from the project's directory
  to install the program on your computer
- set the environment variables, then enter
$ flask run
This will start the webserver

## To reset the database
flask init-db

## To run the server
flask run

## To use the clean_code.py devtool
REQUIRES: autopep8 and pycodestyle installed through pip
from the home directory:
$ python devtools/clean_code.py
Please fix any coding/style errors that it outputs before
submitting to the repo, most will be automatically handled
by autopep8
