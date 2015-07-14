#!/bin/bash

set -o nounset

dir=$1
host="${2:-$RADISH_SERVER_HOST}"
port="${3:-$RADISH_SERVER_PORT}"
localsoftlink="${4:-}"

flags=""

if [ -n $localsoftlink ]; then
    flags+=--localsoftlink
fi

cwd=`pwd`

pushd $RACO_HOME/c_test_environment

for tf in $dir/*.tbl; do
    name=$(basename "$tf" .tbl)
    echo "ingesting $tf as relation $name"
    python grappa_ingest.py -i $tf -c $cwd/catalog.py -n "$name" -s grappa --host=$host --port=$port $flags --storage=binary --delim="|"
done

popd
