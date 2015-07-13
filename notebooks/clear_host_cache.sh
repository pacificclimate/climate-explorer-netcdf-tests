while sleep 1; do
  ls watch/*.tmp | entr -r sh -c 'echo 3 >/proc/sys/vm/drop_caches' && rm ./watch/*.tmp
done
