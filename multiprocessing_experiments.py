import multiprocessing as mp
from multiprocessing import Process, Pipe, Array, Manager, Pool

import os
import re
from collections import Counter

import timeit

from text_analysis import list_texts, open_file, get_words


def get_freq_words(words, num):
    return Counter(words).most_common(num)

def getFreqWordsFromText(text, num):
    text = open_file(text)
    words = get_words(text)
    freqs = get_freq_words(words, num)
    return freqs

def getTitleFreqs(text, num):
    title = os.path.basename(text)
    freqs = getFreqWordsFromText(text, 1)
    return (title, freqs)


def send_pipe(text, conn):
    title, freqs = getTitleFreqs(text, 1)
    conn.send((title, freqs))
    conn.close()

def send_queue(text, q):
    title, freqs = getTitleFreqs(text, 1)
    q.put((title, freqs))

def shared_dict(text, container):
    title, freqs = getTitleFreqs(text, 1)
    container[title] = freqs

def freqsPerText(text):
    title, freqs = getTitleFreqs(text, 1)
    return (title, freqs)


texts = list_texts(os.path.join(os.getcwd(), 'texts'))

def multiprocess_pipe():
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
    return results

def multiprocess_manager():
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

        return container

def multiprocess_queue():
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
    return results

def multiprocess_pool_sync():
    # In this function the apply() method creates a lock that prevents more than the specified number of
    # processes to take place at the same time. In this case, only 10 processes can be active at the same
    # time.
    jobs = []
    pool = Pool(processes=10)
    results = [pool.apply(func=freqsPerText, args=(text,)) for text in texts]
    print('Finished processing texts with Pool')
    print('Pool returned ', len(results), 'results')
    return results

def multiprocess_pool_async():
    jobs = []
    pool = Pool(processes=10)
    results = [pool.apply_async(func=freqsPerText, args=(text,)) for text in texts]
    output = [p.get() for p in results]
    print('Finished processing texts with Pool async')
    print('Pool async returned ', len(output), 'results')
    return output


if __name__ == '__main__':
    print(timeit.timeit('multiprocess_pipe()', setup='from __main__ import multiprocess_pipe', number=1))
    print(timeit.timeit('multiprocess_manager()', setup='from __main__ import multiprocess_manager', number=1))
    print(timeit.timeit('multiprocess_queue()', setup='from __main__ import multiprocess_queue',number=1))
    print(timeit.timeit('multiprocess_pool_sync()', setup='from __main__ import multiprocess_pool_sync', number=1))
    print(timeit.timeit('multiprocess_pool_async()', setup='from __main__ import multiprocess_pool_async', number=1))















        


    
