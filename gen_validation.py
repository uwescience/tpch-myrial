import subprocess
import sys
import os

# TPC-H qgen generates a query from a query template
tpch_utils = "/Users/brandon/escience/tpch_2_17_0/dbgen"
qgen = './qgen'

# used to point qgen to the query templates directory
env = os.environ.copy()
env['DSS_QUERY'] = '/Users/brandon/escience/tpch-radish/templates'

cwd = os.getcwd()

def generate(query):
    intermf = '{cwd}/_q{query}.myl'.format(cwd=cwd, query=query)
    resultf = '{cwd}/q{query}.myl'.format(cwd=cwd, query=query)
    
    subprocess.check_call('cd {path}; {qgen} -d {query} >{of}'.format(path=tpch_utils, qgen=qgen, query=query, of=intermf), shell=True, env=env, stderr=sys.stdout)

    # qgen puts in windows line endings ^M, remove them
    subprocess.check_call("sed 's/{cr}//g' <{inf} >{of}".format(of=resultf, inf=intermf, query=query, cr=chr(13)), shell=True, stderr=sys.stdout)


for q in range(1,22+1):
    generate(q)
