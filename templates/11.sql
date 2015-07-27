-- $ID$
-- TPC-H/TPC-R Important Stock Identification Query (Q11)
-- Functional Query Definition
-- Approved February 1998
partsupp = scan('partsupp');
supplier = scan('supplier');
nation = scan('nation');

val_per_part = select
	ps_partkey,
	sum(ps_supplycost * ps_availqty) as value
from
	partsupp,
	supplier,
	nation
where
	ps_suppkey = s_suppkey
	and s_nationkey = n_nationkey
	and n_name = ':1';
--group by  -- not needed in myriaL
--	ps_partkey 

val_total_frac  = 
			select
				sum(ps_supplycost * ps_availqty) * :2 as frac_total
			from
				partsupp,
				supplier,
				nation
			where
				ps_suppkey = s_suppkey
				and s_nationkey = n_nationkey
				and n_name = ':1';

--return those with a significant fraction of total
q11 = 
    select 
        ps_partkey,
        value
    from
        val_per_part,
        val_total_frac
    where 
        value > frac_total;

--order by  --TODO
--	value desc;

store(q11, q11);
