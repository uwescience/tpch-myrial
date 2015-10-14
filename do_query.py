import argparse
import sys
import subprocess
from contextlib import contextmanager
import os


@contextmanager
def pushd(newDir):
    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)

if __name__ == "__main__":
    RACO_HOME = os.environ['RACO_HOME']
    GRAPPA_HOME = os.environ['GRAPPA_HOME']
    TPCH_RADISH = os.environ['HOME']+"/escience/tpch-radish"


    p = argparse.ArgumentParser(prog=sys.argv[0])
    p.add_argument("querynum", help="tpch query number")
    p.add_argument("--no-regenerate", action="store_true", dest="no_regenerate", help="Do not re-run Raco on the query if the exe already exists")
    p.add_argument("--compiler", dest="compiler", default="push", help="Radish compilation strategy {push,iterator}")
    p.add_argument("--build-mode", dest="build_mode", default="Release", help="Grappa build mode {Release,Debug}")
    p.add_argument("--make-parallelism", dest="make_parallelism", default="8", help="Argument to make -j")
    p.add_argument("--configure-command", dest="configure", default="grappa_configure", help="command to configure grappa on your system; defaults to 'grappa_configure'")
    p.add_argument("--plan-info", action="store_true", dest="plan_info", help="whether to store plan info to plan.db")

    args = p.parse_args(sys.argv[1:])

    query = "q{}".format(args.querynum)

    if args.compiler == 'iterator':
        source_name = 'grappa_tpc_iter_{}'.format(query)
    else:
        source_name = 'grappa_tpc_{}'.format(query)

    build_dir = "{GRAPPA_HOME}/build/Make+{mode}/applications/join".format(GRAPPA_HOME=GRAPPA_HOME, mode=args.build_mode)

    with pushd(RACO_HOME):

        # Radish
        if (not args.no_regenerate) or (not os.path.isfile("{d}/{f}.exe".format(d=build_dir, f=source_name))):
            subprocess.check_calll("""PYTHONPATH=. scripts/myrial -c \
            --catalog {TPCH_RADISH}/catalog.py {plan_info} \
            {TPCH_RADISH}/{query}.myl \
            --key=scan_array_repr --value=symmetric_array \
            --key=compiler --value={compiler}
            """.format(TPCH_RADISH=TPCH_RADISH,
                       query=query,
                       compiler=args.compiler, plan_info="--plan-info=plan.db" if args.plan_info else ""), shell=True)

            subprocess.check_call("""mv {query}.cpp \
            {GRAPPA_HOME}/applications/join/{source_name}.cpp
            """.format(query=query,
                       GRAPPA_HOME=GRAPPA_HOME,
                       source_name=source_name), shell=True)

    with pushd(build_dir):

        # compile cpp
        if not os.path.isfile("{}.exe".format(source_name)):
            subprocess.check_call("{c} --mode={mode}".format(c=args.configure, mode=args.build_mode), shell=True)

        subprocess.check_call("make -j {make_parallelism} {source_name}.exe".format(make_parallelism=args.make_parallelism, source_name=source_name),
                              shell=True)



