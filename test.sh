#!/bin/bash

pushd `dirname $0` > /dev/null
SCRIPT_PATH=`pwd`
popd > /dev/null

python -m unittest tests.test_account
python -m unittest tests.test_message
python -m unittest tests.test_number
