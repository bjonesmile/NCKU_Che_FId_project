import multiprocessing as mp
from multiprocessing import Pool, TimeoutError
import time
import os
import numpy as np
from itertools import product

def func(x1,x2):
    print(f"multi-process ID: {os.getpid()}")
    return x1*x2

def f(x):
    return x*x

def show_curPID(get_result):
    print(f"multi-process result: {get_result} ID: {os.getpid()}")

def merge_names(a, b):
    return '{} & {}'.format(a, b)

if __name__ == '__main__':
    # start 4 worker processes
    num_cores = int(mp.cpu_count())
    print(num_cores)
    ary1 = np.random.randint(10, size=(10,2))
    print(ary1)
    args = ary1
    print("MAIN process ID: ",os.getpid())
    with Pool(processes=num_cores) as pool:
        MapResult = pool.starmap_async(func, args, callback= show_curPID)
        pool.close()
        pool.join()

        result = MapResult.get()
        print(result)

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")