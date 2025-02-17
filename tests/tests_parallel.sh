#!/bin/bash

if [ ! -z $1 ] 
then 
	# test pattern was specified 
	echo 'Run unittests with pattern '$1':'
    ./run_tests.py --unit --runslow --parallel --pattern "$1"
else
	# test pattern was not specified
	echo 'Run all unittests:'
    ./run_tests.py --unit --parallel
fi
