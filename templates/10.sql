-- $ID$
-- TPC-H/TPC-R Returned Item Reporting Query (Q10)
-- Functional Query Definition
-- Approved February 1998

customer = scan('customer');
orders = scan('orders');
lineitem = scan('lineitem');
nation = scan('nation');

q10 = select
	c_custkey,
	c_name,
	sum(l_extendedprice * (1 - l_discount)) as revenue,
	c_acctbal,
	n_name,
	c_address,
	c_phone,
	c_comment
from
	customer,
	orders,
	lineitem,
	nation
where
	c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate >= ':1'
	and o_orderdate < '1994-01-01' -- date ':1' + interval '3' month
	and l_returnflag = 'R'
	and c_nationkey = n_nationkey;
--group by     -- not needed by MyriaL
--	c_custkey,
--	c_name,
--	c_acctbal,
--	c_phone,
--	n_name,
--	c_address,
--	c_comment
--order by       --TODO
--	revenue desc;

store(q10, q10);
