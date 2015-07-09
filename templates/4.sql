lineitem = scan('lineitem');
orders = scan('orders');

-- $ID$
-- TPC-H/TPC-R Order Priority Checking Query (Q4)
-- Functional Query Definition
-- Approved February 1998
exist = select 
    o_orderkey as e_key,
    COUNT(o_orderkey) as e_count
    from lineitem,
         orders
    where
	    l_orderkey = o_orderkey
	    and l_commitdate < l_receiptdate;

q4 = select 
    o_orderpriority,
	count(o_orderpriority) as order_count
    from
        orders,
        exist
    where
        e_key = o_orderkey
        and o_orderdate >= ':1'
        and o_orderdate < '1993-10-01' -- ':1' + interval '3' month
        and e_count > 0;
    
--group by            -- not needed in myriaL
--	o_orderpriority
--order by
--	o_orderpriority;

store(q4, q4);
