set -o nounset

pushd $RACO_HOME

qn=$1

q=q$1

PYTHONPATH=. scripts/myrial -c --catalog ~/escience/tpch-radish/catalog.py ~/escience/tpch-radish/$q.myl  --key=scan_array_repr --value=symmetric_array
mv $q.cpp ~/escience/ci-raco/grappa/applications/join/grappa_tpc_$q.cpp

pushd  ~/escience/ci-raco/grappa/build/Make+Release/applications/join

# first time building this query exe so need to reconfigure
if [[ ! -a grappa_tpc_$q.exe ]]; then
    grappa_configure
fi

make -j grappa_tpc_$q.exe

popd # .../join

popd # $RACO_HOME
