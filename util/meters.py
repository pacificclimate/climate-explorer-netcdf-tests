from time import time
from contextlib import ContextDecorator

import numpy as np

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
