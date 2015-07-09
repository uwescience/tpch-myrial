-- $ID$
-- TPC-H/TPC-R National Market Share Query (Q8)
-- Functional Query Definition
-- Approved February 1998
part = scan('part');
supplier = scan('supplier');
lineitem = scan('lineitem');
orders = scan('orders');
customer = scan('customer');
nation = scan('nation');
region = scan('region');
	
all_nations = 
		select
			year(o_orderdate) as o_year,
			l_extendedprice * (1 - l_discount) as volume,
			n2.n_name as nation
		from
			part,
			lineitem,     -- swapped from 8.sql for join order
			supplier,
			orders,
			customer,
			nation n1,
			nation n2,
			region
		where
			p_partkey = l_partkey
			and s_suppkey = l_suppkey
			and l_orderkey = o_orderkey
			and o_custkey = c_custkey
			and c_nationkey = n1.n_nationkey
			and n1.n_regionkey = r_regionkey
			and r_name = ':2'
			and s_nationkey = n2.n_nationkey
			and o_orderdate >= '1995-01-01' 
            and o_orderdate <= '1996-12-31'
			and p_type = ':3';

q8 = select
	o_year,
	sum(case
		when nation = ':1' then volume
		else 0.0
	end) / sum(volume) as mkt_share
from
    all_nations;
--group by  -- not needed for MyriaL
--	o_year
--order by   -- TODO
--	o_year;

store(q8, q8);
