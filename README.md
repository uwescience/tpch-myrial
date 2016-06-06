# tpch-radish

## Setup

`tpch-radish` requires TPC-H qgen to generate SQL queries and [Raco](https://github.com/uwescience/raco) to generate the Grappa code.

- [Download qgen](http://www.tpc.org/tpch/tools_download/dbgen-download-request.asp)
- Install Raco by following its README.md and then make sure to set `RACO_HOME` to the directory of your Raco

## Generate the queries

```bash
$ python gen_validation.py
```

## See the plan of a query

```bash
$ $RACO_HOME/scripts/myrial [flag] q1.myl
```

Run `$RACO_HOME/scripts/myrial -h` for documentation about the different kinds of output.


## Compile the queries to Grappa (Radish) programs

```bash
$ python do_all_queries_py.sh
```
