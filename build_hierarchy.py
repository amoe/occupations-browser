#! /usr/bin/env python3

import json
import sys
import functools
import pprint

def flip(func):
    @functools.wraps(func)
    def newfunc(x, y):
        return func(y, x)
    return newfunc

def foldr(func, acc, xs):
    return functools.reduce(flip(func), reversed(xs), acc)

def reduction(v, acc):
    ret = {'token': v}

    if acc is not None:
        ret['children'] = [acc]

    return ret

def stratify(sentence):
    return foldr(reduction, None, sentence)

class HierarchyBuilder(object):
    def run(self, args):
        roots = {}

        json_file = args[0]
        all_sentences = json.load(open(json_file, 'r'))
        
        for sentence in all_sentences:
            for word in sentence:
                roots[word] = stratify(sentence)

        pprint.pprint(roots)

if __name__ == '__main__':
    obj = HierarchyBuilder()
    obj.run(sys.argv[1:])
