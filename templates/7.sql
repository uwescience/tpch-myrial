-- $ID$
-- TPC-H/TPC-R Volume Shipping Query (Q7)
-- Functional Query Definition
-- Approved February 1998
supplier = scan('supplier');
lineitem = scan('lineitem');
orders = scan('orders');
customer = scan('customer');
nation = scan('nation');

shipping =
		select
			n1.n_name as supp_nation,
			n2.n_name as cust_nation,
			year(l_shipdate) as l_year,
			l_extendedprice * (1 - l_discount) as volume
		from
			supplier,
			lineitem,
			orders,
			customer,
			nation n1,
			nation n2
		where
			s_suppkey = l_suppkey
			and o_orderkey = l_orderkey
			and c_custkey = o_custkey
			and s_nationkey = n1.n_nationkey
			and c_nationkey = n2.n_nationkey
			and (
				(n1.n_name = ':1' and n2.n_name = ':2')
				or (n1.n_name = ':2' and n2.n_name = ':1')
			)
			and l_shipdate >= '1995-01-01' 
            and l_shipdate <= '1996-12-31';

q7 = select
	supp_nation,
	cust_nation,
	l_year,
	sum(volume) as revenue
from
    shipping;

--group by        -- not needed in MyriaL
--	supp_nation,
--	cust_nation,
--	l_year
--order by       TODO
--	supp_nation,
--	cust_nation,
--	l_year;

store(q7, q7);
