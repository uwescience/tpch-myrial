-- $ID$
-- TPC-H/TPC-R Large Volume Customer Query (Q18)
-- Function Query Definition
-- Approved February 1998
customer = scan('customer');
orders = scan('orders');
lineitem = scan('lineitem');
		
grouped_order_key =
select
    l_orderkey,
    sum(l_quantity) as l_quantity_sum
from
    lineitem;
--group by         -- implemented as groupby+select
--    l_orderkey having
--        sum(l_quantity) > :1

interesting_orders = 
select
    l_orderkey as io_orderkey
from
    grouped_order_key
where
    l_quantity_sum > :1;


q18 = 
select
	c_name,
	c_custkey,
	o_orderkey,
	o_orderdate,
	o_totalprice,
	sum(l_quantity)
from
	customer,
	orders,
	lineitem,
    interesting_orders
where
	o_orderkey = io_orderkey -- in (subquery)
	and c_custkey = o_custkey
	and o_orderkey = l_orderkey;
--group by    -- not needed by myriaL
--	c_name,
--	c_custkey,
--	o_orderkey,
--	o_orderdate,
--	o_totalprice
--order by        -- TODO
--	o_totalprice desc,
--	o_orderdate;

store(q18, q18);
