import multiprocessing
import os

from text_analysis import list_texts, find_pattern

def run_processes():
    jobs = []
    
    path = os.path.join(os.getcwd(), 'texts')
    pattern = re.compile(r'\w{4}')
    texts = list_texts(path)
    
    for text in texts:
        process = multiprocessing.Process(target=find_pattern, args=(pattern, text))
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
