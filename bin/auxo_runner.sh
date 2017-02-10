#!/bin/bash

TOP=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)

# only run if environment settings are available
#
if [ ! -f "$TOP/bin/auxo_runner.env" ]
then
	echo "no environment settings available."
	exit 1
fi
source "$TOP/bin/auxo_runner.env"

# create the log directory if it doesn't exist
#
if [ ! -d "$LOGDIR" ]
then
	mkdir -p "$LOGDIR"
fi

# create the states directory if it doesn't exist
#
if [ ! -d "$AUXODIR" ]
then
	mkdir -p "$AUXODIR"
fi

# run the auxo python script with the parameters from this script appended.
#
export PYTHONPATH=$TOP
#
$TOP/bin/auxo $* > $LOGDIR/auxo-out.log 2> $LOGDIR/auxo-err.log
