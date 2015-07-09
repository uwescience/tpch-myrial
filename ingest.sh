#!/bin/bash

dir=$1
host="${2:-sampa-gw.cs.washington.edu}"
port="${3:-1337}"

cwd=`pwd`

pushd $RACO_HOME/c_test_environment

for tf in $dir/*.tbl; do
    name=$(basename "$tf" .tbl)
    echo "ingesting $tf as relation $name"
    python grappa_ingest.py -i $tf -c $cwd/catalog.py -n "$name" -s grappa --host=$host --port=$port --storage=binary --delim="|"
done

popd
