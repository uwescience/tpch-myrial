-- $ID$
-- TPC-H/TPC-R Shipping Modes and Order Priority Query (Q12)
-- Functional Query Definition
-- Approved February 1998
orders = scan('orders');
lineitem = scan('lineitem');

q12 = select
	l_shipmode,
	sum(case
		when o_orderpriority = '1-URGENT'
			or o_orderpriority = '2-HIGH'
			then 1
		else 0
	end) as high_line_count,
	sum(case
		when o_orderpriority <> '1-URGENT'
			and o_orderpriority <> '2-HIGH'
			then 1
		else 0
	end) as low_line_count
from
	orders,
	lineitem
where
	o_orderkey = l_orderkey
	and (l_shipmode = ':1' or l_shipmode = ':2') -- in (':1', ':2')
	and l_commitdate < l_receiptdate
	and l_shipdate < l_commitdate
	and l_receiptdate >= ':3'
	and l_receiptdate < '1995-01-01'; -- date ':3' + interval '1' year
-- group by  -- not needed by myriaL
-- 	l_shipmode
-- order by  -- TODO
-- 	l_shipmode;

store(q12, q12);
