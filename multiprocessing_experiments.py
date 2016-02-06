import multiprocessing as mp
from multiprocessing import Process, Pipe, Array, Manager

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

def send_queue(text, q):
    title = os.path.basename(text)
    freqs = getFreqWordsFromText(text, 1)
    q.put((title, freqs))

def shared_dict(text, container):
    title = os.path.basename(text)
    container[title] = getFreqWordsFromText(text, 1)



if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f2, args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()

    texts = list_texts(os.path.join(os.getcwd(), 'texts'))
    freq_words_per_text = {}

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

        print('Finished processing texts')

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
print('Finished processing texts')
print('Queue returned ', len(results), 'results')


        


    
