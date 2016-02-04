import multiprocessing as mp
from multiprocessing import Process
import os
from collections import Counter

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('funciton f')
    print('hello', name)

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
    q = mp.Queue()
    p = Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
    
