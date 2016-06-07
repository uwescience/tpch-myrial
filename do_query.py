import argparse
import sys
import subprocess
from contextlib import contextmanager
import os
from timeit import repeat

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
    p.add_argument("--join-type", dest="join_type", default="GrappaHashJoin", help="Radish join type")
    p.add_argument("--build-mode", dest="build_mode", default="Release", help="Grappa build mode {Release,Debug}")
    p.add_argument("--groupby-semantics", dest="groupby_semantics", default="global", help="{global, partition}")
    p.add_argument("--make-parallelism", dest="make_parallelism", default="", help="Argument to make -j")
    p.add_argument("--configure-command", dest="configure", default="grappa_configure", help="command to configure grappa on your system; defaults to 'grappa_configure'")
    p.add_argument("--plan-info", action="store_true", dest="plan_info", help="whether to store plan info to plan.db")
    p.add_argument("--generate-only", action="store_true", dest="generate_only", help="only run Raco")
    p.add_argument("--timing", action="store_true", dest="timing", help="keep timing")

    args = p.parse_args(sys.argv[1:])

    query = "q{}".format(args.querynum)

    if args.compiler == 'iterator':
        source_name = 'grappa_tpc_iter_{}'.format(query)
    elif args.compiler == 'push':
        source_name = 'grappa_tpc_{}'.format(query)
    else:
        raise ValueError("unsupported value for compiler: {}".format(args.compiler))

    if args.join_type == 'GrappaSymmetricHashJoin':
        source_name = source_name + '_sym'
    elif args.join_type == 'GrappaOverSynchronizedSymmetricHashJoin':
        source_name = source_name + '_osym'

    if args.groupby_semantics == 'partition':
        source_name = source_name + '_gbp'

    build_dir = "{GRAPPA_HOME}/build/Make+{mode}/applications/join".format(GRAPPA_HOME=GRAPPA_HOME, mode=args.build_mode)

    with pushd(RACO_HOME):

        # Radish
        if (not args.no_regenerate) or (not os.path.isfile("{d}/{f}.exe".format(d=build_dir, f=source_name))):
            def raco():
                subprocess.check_call("""PYTHONPATH=. scripts/myrial -c \
                --catalog {TPCH_RADISH}/catalog.py {plan_info} \
                {TPCH_RADISH}/{query}.myl \
                --key=scan_array_repr --value=symmetric_array \
                --key=compiler --value={compiler} \
                --key=join_type --value={join_type} \
                --key=groupby_semantics --value={groupby_semantics} 
                """.format(TPCH_RADISH=TPCH_RADISH,
                           query=query,
                           plan_info="--plan-info=plan.db" if args.plan_info else "",
                           compiler=args.compiler,
                           join_type=args.join_type,
                           groupby_semantics=args.groupby_semantics), shell=True)

            if args.timing:
                raco_times = repeat(raco, repeat=3, number=1)
            else:
                raco()

            subprocess.check_call("""mv {query}.cpp \
            {GRAPPA_HOME}/applications/join/{source_name}.cpp
            """.format(query=query,
                       GRAPPA_HOME=GRAPPA_HOME,
                       source_name=source_name), shell=True)

    if not args.generate_only:
        with pushd(build_dir):

            # compile cpp
            if not os.path.isfile("{}.exe".format(source_name)):
                subprocess.check_call("{c} --mode={mode}".format(c=args.configure, mode=args.build_mode), shell=True)

            def grappa_compile():
                subprocess.check_call("make -j {make_parallelism} {source_name}.exe".format(make_parallelism=args.make_parallelism, source_name=source_name),
                        shell=True)

            if args.timing:
                # do it once to compile dependences
                grappa_compile()

                def touch_first():
                    subprocess.check_call("touch {GRAPPA_HOME}/applications/join/{source_name}.cpp".format(query=query, GRAPPA_HOME=GRAPPA_HOME, source_name=source_name), shell=True)
                    grappa_compile()

                grappa_compile_times = repeat(touch_first, repeat=3, number=1)
            else:
                grappa_compile()



    if args.timing:
        import dataset
        db = dataset.connect('sqlite:///compilation.db')
        params = { 'query': query,
                   'compiler': args.compiler,
                   'join_type': args.join_type,
                   'groupby_semantics': args.groupby_semantics,
                   }

        for t in raco_times:
            d = params.copy()
            d.update({'raco_time': t}) # timeit gets the min
            db['raco'].insert(d)
            
        compiler_version = subprocess.check_output('gcc -v 2>&1 | grep version', shell=True)
        for t in grappa_compile_times:
            d = params.copy()
            d.update({'grappa_compile_time': t, 
                      'compiler_version': compiler_version})
            db['compiler'].insert(d)

