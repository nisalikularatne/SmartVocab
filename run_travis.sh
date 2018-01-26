#!/usr/bin/env bash
python tests/test_WordModel.py > /dev/null &
nosetests --with-coverage