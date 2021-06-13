#!/bin/bash

# Turn off posix mode since it does not allow process substitution
set +o posix

if [ "$1" = 'eddy-python-flink-bridge' ]; then
    exec celery worker -A app -l INFO -Q flink
fi

exec "$@"
