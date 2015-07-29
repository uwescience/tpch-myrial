-- $ID$
-- TPC-H/TPC-R Discounted Revenue Query (Q19)
-- Functional Query Definition
-- Approved February 1998
lineitem = scan('lineitem');
part = scan('part');

q19 = 
select
	sum(l_extendedprice* (1 - l_discount)) as revenue
from
	part,
	lineitem
where
    p_partkey = l_partkey and (
        (
            p_brand = ':1'
            and (p_container = 'SM CASE' or p_container = 'SM BOX' or p_container = 'SM PACK' or p_container = 'SM PKG')
            and l_quantity >= :4 and l_quantity <= :4 + 10
            and (p_size >= 1 and p_size <= 5)
            and (l_shipmode = 'AIR' or l_shipmode = 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
        or
        (
            p_brand = ':2'
            and (p_container = 'MED BAG' or p_container = 'MED BOX' or p_container = 'MED PKG' or p_container = 'MED PACK')
            and l_quantity >= :5 and l_quantity <= :5 + 10
            and (p_size >= 1 and p_size <= 10)
            and (l_shipmode = 'AIR' or l_shipmode = 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
        or
        (
            p_brand = ':3'
            and (p_container = 'LG CASE' or p_container = 'LG BOX' or p_container = 'LG PACK' or p_container = 'LG PKG')
            and l_quantity >= :6 and l_quantity <= :6 + 10
            and (p_size >= 1 and p_size <= 15)
            and (l_shipmode = 'AIR' or l_shipmode = 'AIR REG')
            and l_shipinstruct = 'DELIVER IN PERSON'
        )
    );

store(q19, q19);
