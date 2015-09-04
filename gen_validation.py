import subprocess

import sys
import os

import argparse

# TPC-H qgen generates a query from a query template
_qgen = './qgen'

if __name__ == '__main__':
    env = os.environ.copy()

    p = argparse.ArgumentParser(prog=sys.argv[0])
    p.add_argument('--tpch', dest='tpch', default="{HOME}/escience/tpch_2_17_0".format(HOME=env['HOME']))

    args = p.parse_args(sys.argv[1:])


    tpch_utils = args.tpch + '/dbgen'

    here = os.path.abspath(os.path.dirname(__file__))

    # used to point qgen to the query templates directory
    env['DSS_QUERY'] = '{here}/templates'.format(here=here)

    cwd = os.getcwd()

    def generate(query):
        intermf = '{cwd}/_q{query}.myl'.format(cwd=cwd, query=query)
        resultf = '{cwd}/q{query}.myl'.format(cwd=cwd, query=query)

        try:
            subprocess.check_call('cd {path}; {qgen} -d {query} >{of}'.format(path=tpch_utils, qgen=_qgen, query=query, of=intermf), shell=True, env=env, stderr=sys.stdout)
        except subprocess.CalledProcessError as e:
           sys.stderr.write('WARN: query {0} failed to generate: {1}\n'.format(query, e))
           return False

        # qgen puts in windows line endings ^M, remove them;
        # also qgen doesn't allow ':' so sub them in for __C__
        subprocess.check_call("sed -e 's/{cr}//g' -e 's/__C__/:/g' <{inf} >{of}".format(of=resultf, inf=intermf, query=query, cr=chr(13)), shell=True, stderr=sys.stdout)
        os.remove(intermf)

        return True

    for q in range(1, 22+1):
        generate(q)
