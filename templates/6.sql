lineitem = scan('lineitem');

-- $ID$
-- TPC-H/TPC-R Forecasting Revenue Change Query (Q6)
-- Functional Query Definition
-- Approved February 1998
q6 = select
	sum(l_extendedprice * l_discount) as revenue
from
	lineitem
where
	l_shipdate >= ':1'
	and l_shipdate < '1995-01-01' --date ':1' + interval '1' year
	and l_discount >= :2 - 0.01 
    and l_discount <= :2 + 0.01
	and l_quantity < :3;

store(q6, q6);
