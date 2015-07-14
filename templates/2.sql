part = scan('part');
lineitem = scan('lineitem');
supplier = scan('supplier');
nation = scan('nation');
region = scan('region');
partsupp = scan('partsupp');

-- NOTES: we might rewrite the myl query to force some optimizations:
-- from TPC-H analyzed:
-- CP5.2: Q2 shows a frequent pattern: a correlated subquery which computes an aggregate that is subsequently used in a selection predicate of a similarly looking outer query ("select the minimum cost part supplier for a certain part"). Here the outer query has additional restrictions (on part type and size) that are not present in the correlated subquery, but should be propagated to it. 

-- note that since Raco doesn't support correlated subqueries,
-- we need to rewrite 2.sql so that the subquery groups by partkey and selects only relevant parts
-- then we add a join by that partkey in the outer query
-- (see min_partkey=p_partkey)

min_ps_supplycost_relation = select
			p_partkey as min_partkey,
            min(ps_supplycost) as min_ps_supplycost
		from
            part,    
			partsupp,
			supplier,
			nation,
			region
		where
			p_partkey = ps_partkey
	    and p_size = :1   -- [1 , 50]
	and p_type like '%:2' -- syllable3
			and s_suppkey = ps_suppkey
			and s_nationkey = n_nationkey
			and n_regionkey = r_regionkey
			and r_name = ':3';

q2 = select
	s_acctbal,
	s_name,
	n_name,
	p_partkey,
	p_mfgr,
	s_address,
	s_phone,
	s_comment
from
	part,
	partsupp,
	supplier,
	nation,
	region,
    min_ps_supplycost_relation
where
	p_partkey = ps_partkey
	and s_suppkey = ps_suppkey
	and p_size = :1   -- [1 , 50]
	and p_type like '%:2' -- syllable3
	and s_nationkey = n_nationkey
	and n_regionkey = r_regionkey
	and r_name = ':3' -- R_NAME
	and ps_supplycost = min_ps_supplycost
    and min_partkey = p_partkey;
--order by
--	s_acctbal desc,
--	n_name,
--	s_name,
--	p_partkey;


store(q2, q2);
