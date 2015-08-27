for i in `seq 1 22`; do
    python do_query.py $i "$@"
done
