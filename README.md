# tpch-myrial

This is an implementation of TPC-H in the [MyriaL language](http://myria.cs.washington.edu/docs/myrial.html). You can use it to generate TPC-H query plans for any back end of the [Raco relational algebra compiler](https://github.com/uwescience/raco).

## Setup

`tpch-myrial` requires TPC-H qgen to generate SQL queries and [Raco](https://github.com/uwescience/raco) to generate the query plans.

- [Download qgen](http://www.tpc.org/tpch/tools_download/dbgen-download-request.asp)
- Install Raco by following its README.md and then make sure to set `RACO_HOME` to the directory of your Raco

## Generate the queries

The queries are expressed as TPC-H `qgen` template files. The following command will run `qgen` on all the templates
using the test parameters from the TPC-H specification.

```bash
python gen_validation.py
```

## See the plan of a query

```bash
$RACO_HOME/scripts/myrial [flag] q1.myl
```

Run `$RACO_HOME/scripts/myrial -h` for documentation about the different kinds of output.


## Compile the queries to Grappa (Radish) programs

```bash
python do_all_queries_py.sh COMPILER_FLAGS
```

## Caveats

- The queries are currently modified to omit sorting (`ORDER BY`) because MyriaL does not yet support ORDER BY (for no particular reason).
