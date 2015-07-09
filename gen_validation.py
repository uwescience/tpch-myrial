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
    
    subprocess.check_call('cd {path}; {qgen} -d {query} >{cwd}/q{query}.myl'.format(path=tpch_utils, qgen=qgen, query=query, cwd=cwd), shell=True, env=env, stderr=sys.stdout)

for q in range(1,2+1):
    generate(q)
