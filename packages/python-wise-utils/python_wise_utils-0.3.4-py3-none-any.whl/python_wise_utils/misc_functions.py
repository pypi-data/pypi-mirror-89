from itertools import zip_longest
from pprint import pprint


def _grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def pager(iterable, length=20):
    for i in _grouper(iterable, length):
        pprint([x for x in i if x])
        if input(':'):
            break

