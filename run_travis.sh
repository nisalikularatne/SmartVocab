#!/usr/bin/env bash
python engine/domain/WordModel.py > /dev/null &
nosetests --with-coverage