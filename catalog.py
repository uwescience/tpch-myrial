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
      ('p_size', 'LONG_TYPE'),
      ('p_container', 'STRING_TYPE'),
      ('p_retailprice', 'DOUBLE_TYPE'),
      ('p_comment', 'STRING_TYPE')],

}
