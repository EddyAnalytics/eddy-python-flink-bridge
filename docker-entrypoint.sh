#!/bin/bash
_FLINK_HOME_DETERMINED=1
. "$FLINK_HOME"/bin/config.sh

FLINK_CLASSPATH=`constructFlinkClassPath`
PYTHON_JAR_PATH=`echo "$FLINK_OPT_DIR"/flink-python*.jar`
PYFLINK_PYTHON="${PYFLINK_PYTHON:-"python"}"

# So that python can find out Flink's Jars
export FLINK_BIN_DIR=$FLINK_BIN_DIR
export FLINK_HOME

# Add pyflink & py4j to PYTHONPATH
export PYTHONPATH="$FLINK_OPT_DIR/python/pyflink.zip:$PYTHONPATH"
PY4J_ZIP=`echo "$FLINK_OPT_DIR"/python/py4j-*-src.zip`
export PYTHONPATH="$PY4J_ZIP:$PYTHONPATH"

# Turn off posix mode since it does not allow process substitution
set +o posix

export SUBMIT_ARGS="remote -m $HOST:$PORT -d"
if [ "$1" = 'eddy-python-flink-bridge' ]; then
    exec celery worker -A app -l INFO -Q flink
fi

exec "$@"
