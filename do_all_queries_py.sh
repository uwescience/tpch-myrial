for i in `seq 1 20`; do   #21,22
    python do_query.py $i "$@"
done
