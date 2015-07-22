from time import time, sleep
from contextlib import ContextDecorator

import numpy as np
import os

class ThroughputMeter(ContextDecorator):
    def __enter__(self):
        self.t0 = time()
        return self
    def __exit__(self, *exc):
        self.tn = time()

    def megabytes_per_second(self, array):
        seconds = self.tn - self.t0
        MB = np.prod(array.shape) / 1024 ** 2 * array.dtype.itemsize
        MBps = MB / seconds
        print("{:03.3f} MB in {:03.3} seconds at {:03.3f} MB / sec".format(MB, seconds, MBps))
        return MBps

def clear_host_cache():
    """ Ensures that temp files created for subsequent readout throughput tests read from disk instead of cache. 
        This requires triggering the script clear_host_cache.sh to carry out the clearing of system cache
        by way of modifying a .tmp file in the /app/watch directory, which is linked to a real directory on the host. 
        If you are using this function, make sure to run /path/on/host/to/notebooks/sudo clear_host_cache.sh &> /dev/null on the host before starting 
        the test suite."""
    os.system('touch /app/cc_sig.tmp')

    while True:
        try:
            os.stat('/app/cc_sig.tmp')
        except: # clear_host_cache.sh will delete the temp file after the cache is cleared, which will cause this exception
            print('host cache cleared')
            sleep(0.3) # leave enough time for the host to finish before executing next Python statement
            break
