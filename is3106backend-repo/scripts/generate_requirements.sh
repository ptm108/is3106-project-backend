#!/bin/sh
# generate requirements.txt file from pipfile.lock
pipenv lock --requirements > requirements.txt