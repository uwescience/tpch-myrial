-- $ID$
-- TPC-H/TPC-R Parts/Supplier Relationship Query (Q16)
-- Functional Query Definition
-- Approved February 1998
supplier = scan('supplier');
part = scan('part');
partsupp = scan('partsupp');

withOUT_complaints = 
		select
			s_suppkey as nc_key
		from
			supplier
		where
			not (s_comment like '%Customer%Complaints%');

q16_preproject =
select
	p_brand,
	p_type,
	p_size,
    ps_suppkey, -- distinct ps_suppkey
    count(nc_key) as supplier_cnt_p
	-- groupby(ps_suppkey, count(p_partkey)) to replace count(distinct ps_suppkey) as supplier_cnt
from
	partsupp,
	part,
    withOUT_complaints
where
	p_partkey = ps_partkey
	and (p_brand <> ':1')
	and (not (p_type like ':2%'))
	and (p_size = :3 or p_size = :4 or p_size = :5 or p_size = :6 or p_size = :7 or p_size = :8 or p_size = :9 or p_size = :10)
	and ps_suppkey = nc_key; -- not in with_complaints
--group by     -- not needed by myrial
--	p_brand,
--	p_type,
--	p_size
-- order by       -- TODO
-- 	supplier_cnt desc,
-- 	p_brand,
-- 	p_type,
-- 	p_size;

q16 = select 
	p_brand,
	p_type,
	p_size,
    count(supplier_cnt_p) as supplier_cnt -- all supplier_cnt are 1
from
    q16_preproject;
-- group by
--   ps_suppkey
    

store(q16, q16);
