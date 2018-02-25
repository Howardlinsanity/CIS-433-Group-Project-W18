#!/usr/bin/env bash
SHELL := /bin/bash
# Author(s): Brian + Jamie
# Credit: Based of a makefile originally designed by Michal Young at the UO for CIS 322.

VENV = virtualenv env


# User instructions:
# In order to construct and run this project type "make run" into the shell window
# This should create the virtual environment and install any dependencies,
# finally running the application. connect to the website with the url "https://localhost:PORTNUM"
# The port number should be displayed in the console when building the project.
# To quit the application, simply close out of the window.

# Configuration options
#    Makefile.local is produced by the 'configure' script
#    client_secrets.py must be placed in the secrets directory
#
#Makefile.local: 
#	bash ./configure
#include Makefile.local

# Virtual environment
# To add a dependency to this project:
# create the virtual environment with "make env"
# go into the virtual environment with "source ./env/bin/activate"
# install any new dependencies
# use "make freeze" to write the state to requirements.txt
# get out of the virtual environment with "deactivate"

INVENV = source ./env/bin/activate;

env:
	$(VENV)
	($(INVENV) pip install --upgrade pip; pip install -r requirements.txt) || true

freeze:
	(pip freeze | grep -v "pkg-resources" > requirements.txt) || true

run:	env
	($(INVENV) python2 GUI_app.py) ||  true

jamie: env
	mongod &
	$(INVENV) python2 demos/mongoup.py
	$(INVENV) python2 demos/trial_db.py
	$(INVENV) python2 demos/destroy_db.py
	$(INVENV) python2 demos/trial_db.py


# Run server in background. Be comfortable with killing processes to kill the server before running in background
background: env
	($(INVENV) python2 gui_sandbox/tkinter_sandbox/GUI_app.py) &

# Run test suite. 
# Nosetest will run all files of the form test_*.py

# Will run all functions in all test_*.py files.
# Intended to test data processing functions
test:	env
	$(INVENV) nosetests

# 'clean' should leave the project ready to run
# 'veryclean' will leave project in a state that requires re-running installation and configuration steps
# making the repo very clean before testing and debugging is advised.

clean:
	rm -f *.pyc
	rm -rf __pycache__

veryclean:
	make clean
	rm -f CONFIG.py
	rm -rf env
	rm -f Makefile.local

# Developer tools
#
# when using mastUp and locUp, make sure that the recipe did not fail by reading the last line.
# locUp and mastUp will NOT commit for you. make sure you commit your branch changes.
# if either command fails, check your commits
#
# usage: make BRANCH="branch_name" locUp/mastUp

# updates local directory with most recent code
locUp:
	git checkout ${BRANCH}
	git pull origin ${BRANCH}
	git pull origin master
	git push origin ${BRANCH}

# updates master by merging branch_name with master
mastUp: locUp
	git checkout master
	git pull origin master
	git pull origin ${BRANCH}
	git push origin master
	git checkout ${BRANCH}
	git pull origin master

