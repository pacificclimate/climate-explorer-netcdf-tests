while sleep 1; do
  test -f cc_sig.tmp && echo 3 >/proc/sys/vm/drop_caches && rm cc_sig.tmp && echo "Cache Cleared"
done
