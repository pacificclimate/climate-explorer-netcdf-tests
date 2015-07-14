while sleep 1; do
  ls watch/cc_sig.tmp | entr -r sh -c 'echo 3 >/proc/sys/vm/drop_caches' && rm ./watch/cc_sig.tmp
done
