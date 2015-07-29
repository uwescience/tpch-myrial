-- $ID$
-- TPC-H/TPC-R Top Supplier Query (Q15)
-- Functional Query Definition
-- Approved February 1998
lineitem = scan('lineitem');
supplier = scan('supplier');

revenue:s = 
	select
		l_suppkey as supplier_no,
		sum(l_extendedprice * (1 - l_discount)) as total_revenue
	from
		lineitem
	where
		l_shipdate >= ':1'
		and l_shipdate < '1996-04-01'; --date ':1' + interval '3' month
--	group by         -- not needed by myriaL
--		l_suppkey;

max_total_revenue = 
		select
			max(total_revenue) as m_revenue
		from
			revenue:s;

q15 = select
	s_suppkey,
	s_name,
	s_address,
	s_phone,
	total_revenue
from
	supplier,
	revenue:s,
    max_total_revenue
where
	s_suppkey = supplier_no
	and total_revenue = m_revenue;

--order by      --TODO
--	s_suppkey;

store(q15, q15);
