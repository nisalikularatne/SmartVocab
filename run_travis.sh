#!/usr/bin/env bash
python WordModel.py > /dev/null &
nosetests --with-coverage