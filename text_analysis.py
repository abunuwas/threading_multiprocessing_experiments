import re
from os import listdir
from os.path import isfile, join


def open_file(file):
    return open(file, 'r', encoding='utf-8').read()

def find_pattern(pattern, text):
    text = open_file(text)
    return re.findall(pattern, text)

def list_texts(path):
    return [join(path, f) for f in listdir(path) if isfile(join(path, f)) and f.endswith('.txt')]
