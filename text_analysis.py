import re
from os import listdir
from os.path import isfile, join


def list_texts(path):
    return [join(path, f) for f in listdir(path)
            if isfile(join(path, f)) and f.endswith('.txt')]

def gen_texts(path):
    return (join(path, f) for f in listdir(path)
            if isfile(join(path, f)) and f.endswith('.txt'))

def open_file(file):
    return open(file, 'r', encoding='utf-8').read()



def get_words(text):
    return re.findall('\w+', text)

def find_pattern(pattern, text):
    text = open_file(text)
    return re.findall(pattern, text)

