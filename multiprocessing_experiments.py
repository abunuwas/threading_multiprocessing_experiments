import multiprocessing as mp
from multiprocessing import Process, Pipe, Array, Manager, Pool

import os
import re
from collections import Counter

from text_analysis import list_texts, open_file, get_words


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

def send_pipe(text, conn):
    title = os.path.basename(text)
    freqs = getFreqWordsFromText(text, 1)
    conn.send((title, freqs))
    conn.close()

def send_queue(text, q):
    title = os.path.basename(text)
    freqs = getFreqWordsFromText(text, 1)
    q.put((title, freqs))

def shared_dict(text, container):
    title = os.path.basename(text)
    container[title] = getFreqWordsFromText(text, 1)

def freqsPerText(text):
    title = os.path.basename(text)
    freqs = getFreqWordsFromText(text, 1)
    return (title, freqs)


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f2, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()

    texts = list_texts(os.path.join(os.getcwd(), 'texts'))

    jobs = []
    parent_conn, child_conn = Pipe()
    for text in texts:
        process = Process(target=send_pipe, args=(text, child_conn))
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    results = [parent_conn.recv() for j in jobs]
    print('Finished processing texts with Pipe')
    print('Pipe returned {} results'.format(len(results)))
    for r in results:
        print(r)


    jobs = []
    with Manager() as manager:
        container = manager.dict()
        for text in texts:
            process = Process(target=shared_dict, args=(text, container))
            jobs.append(process)

        for j in jobs:
            j.start()

        for j in jobs:
            j.join()

        print('Finished processing texts with manager.dict')
        print('manager.dict returned ', len(container), 'results')

    jobs = []
    q = mp.Queue()
    for text in texts:
        process = Process(target=send_queue, args=(text, q))
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    results = [q.get() for j in jobs]
    print('Finished processing texts que Queue')
    print('Queue returned ', len(results), 'results')


    jobs = []
    pool = Pool(processes=10)
    results = [pool.apply(func=freqsPerText, args=(text,)) for text in texts]
    print('Finished processing texts with Pool')
    print('Pool returned ', len(results), 'results')


    jobs = []
    pool = Pool(processes=10)
    results = [pool.apply_async(func=freqsPerText, args=(text,)) for text in texts]
    output = [p.get() for p in results]
    print('Finished processing texts with Pool async')
    print('Pool async returned ', len(output), 'results')


        


    
