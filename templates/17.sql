-- $ID$
-- TPC-H/TPC-R Small-Quantity-Order Revenue Query (Q17)
-- Functional Query Definition
-- Approved February 1998
lineitem = scan('lineitem');
part = scan('part');


items = select
    l_quantity,
    l_extendedprice
from
	lineitem,
	part
where
    l_partkey = p_partkey
    and p_brand = ':1'
    and p_container = ':2';

-- using as materialized view may be useful

frac_avg = 
		select
			0.2 * (sum(l_quantity)/count(l_quantity)) as frac_avg_lq -- avg
		from
            items;

q17 =
select
	sum(l_extendedprice) / 7.0 as avg_yearly
from
    items,
    frac_avg
where
	l_quantity < frac_avg_lq;

store(q17, q17);
