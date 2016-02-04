import multiprocessing as mp
from multiprocessing import Process, Pipe

import os
import re
from collections import Counter

from text_analysis import list_texts, open_file, get_words


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

def foo(q):
    q.put('hello')

def f2(conn):
    conn.send([42, None, 'hello'])
    conn.close()


def get_freq_words(words, num):
    return Counter(words).most_common(num)

def getFreqWordsFromText(text, num):
    text = open_file(text)
    words = get_words(text)
    freqs = get_freq_words(words, num)
    return freqs

def send_data(conn, title, freqs):
    conn.send({title: freqs})
    conn.close()


if __name__ == '__main__':
##    info('main line')
##    p = Process(target=f, args=('bob',))
##    p.start()
##    p.join()
##    q = mp.Queue()
##    p = Process(target=foo, args=(q,))
##    p.start()
##    print(q.get())
##    p.join()
    parent_conn, child_conn = Pipe()
    p = Process(target=f2, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()

    texts = list_texts(os.path.join(os.getcwd(), 'texts'))
    freq_words_per_text = {}
    jobs = []
    
    for text in texts:
##        parent_conn, child_conn = Pipe()
        q = mp.Queue()
        process = Process(target=getFreqWordsFromText, args=(text, 1))
        jobs.append(process)

    for j in jobs:
        j.start()
        


    
