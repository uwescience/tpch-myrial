# Schemas corresponding to Myrial examples

{
    'public:adhoc:lineitem' : [
      ('l_orderkey', 'LONG_TYPE'),
      ('l_partkey', 'LONG_TYPE'),
      ('l_suppkey', 'LONG_TYPE'),
      ('l_linenumber', 'LONG_TYPE'),
      ('l_quantity', 'LONG_TYPE'),
      ('l_extendedprice', 'DOUBLE_TYPE'),
      ('l_discount', 'DOUBLE_TYPE'),
      ('l_tax', 'DOUBLE_TYPE'),     
      ('l_returnflag', 'STRING_TYPE'), # only needs to be size 1
      ('l_linestatus', 'STRING_TYPE'), # only needs to be size 1
      ('l_shipdate', 'STRING_TYPE'), # DATE
      ('l_commitdate', 'STRING_TYPE'), # DATE
      ('l_receiptdate', 'STRING_TYPE'), # DATE
      ('l_shipinstruct', 'STRING_TYPE'),
      ('l_shipmode', 'STRING_TYPE'),
      ('l_comment', 'STRING_TYPE')],

    'public:adhoc:part' : [
      ('p_partkey', 'LONG_TYPE'), 
      ('p_name', 'STRING_TYPE'),
      ('p_mfgr', 'STRING_TYPE'),
      ('p_brand', 'STRING_TYPE'),
      ('p_type', 'STRING_TYPE'),
      ('p_size', 'LONG_TYPE'),
      ('p_container', 'STRING_TYPE'),
      ('p_retailprice', 'DOUBLE_TYPE'),
      ('p_comment', 'STRING_TYPE')],

    'public:adhoc:supplier' : [
      ('s_suppkey', 'LONG_TYPE'),
      ('s_name', 'STRING_TYPE'),
      ('s_address', 'STRING_TYPE'),
      ('s_nationkey', 'LONG_TYPE'),
      ('s_phone','STRING_TYPE'),
      ('s_acctbal', 'DOUBLE_TYPE'),
      ('s_comment', 'STRING_TYPE')],

      'public:adhoc:partsupp' : [
      ('ps_partkey',   'LONG_TYPE'),
      ('ps_suppkey', 'LONG_TYPE'),
      ('ps_availqty', 'LONG_TYPE'),
      ('ps_supplycost', 'DOUBLE_TYPE'),
      ('ps_comment', 'STRING_TYPE')],

    'public:adhoc:customer' : [
        ('c_custkey', 'LONG_TYPE'),
        ('c_name', 'STRING_TYPE'),
        ('c_address', 'STRING_TYPE'),
        ('c_nationkey', 'LONG_TYPE'),
        ('c_phone', 'STRING_TYPE'),
        ('c_acctbal', 'STRING_TYPE'),
        ('c_mktsegment', 'STRING_TYPE'),
        ('c_comment', 'STRING_TYPE')],

    'public:adhoc:orders' : [
        ('o_orderkey', 'LONG_TYPE'),
        ('o_custkey', 'LONG_TYPE'),
        ('o_orderstatus', 'STRING_TYPE'), # size 1
        ('o_totalprice', 'STRING_TYPE'),
        ('o_orderdate', 'STRING_TYPE'),
        ('o_orderpriority', 'STRING_TYPE'),
        ('o_clerk', 'STRING_TYPE'),
        ('o_shippriority', 'LONG_TYPE'),
        ('o_comment', 'STRING_TYPE')],

    'public:adhoc:nation' : [
        ('n_nationkey', 'LONG_TYPE'),  # 25 nations
        ('n_name', 'STRING_TYPE'),
        ('n_regionkey', 'LONG_TYPE'),
        ('n_comment', 'STRING_TYPE')],

    'public:adhoc:region' : [
        ('r_regionkey', 'LONG_TYPE'), # 5 regions
        ('r_name', 'STRING_TYPE'),
        ('r_comment', 'STRING_TYPE')],

}
