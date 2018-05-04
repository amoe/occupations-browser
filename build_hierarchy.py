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

def add_sentence(the_root, sentence):
    if sentence:
        this_item = sentence.pop(0)
        
        children = the_root['children']
        
        found = False
        idx = 0
        for child in children:
            if child['token'] == this_item:
                found = True
                break
            idx += 1

        # now we know the index
        if found:
            children[idx]['
            

        


class HierarchyBuilder(object):
    def run(self, args):
        the_root = {'token': 'NONESUCH', 'children': []}

        json_file = args[0]
        all_sentences = json.load(open(json_file, 'r'))
        
        for sentence in all_sentences:
            if sentence[0] != "Queen":
                continue

            # Mutative!
            add_sentence(the_root, sentence)

        pprint.pprint(the_root)

if __name__ == '__main__':
    obj = HierarchyBuilder()
    obj.run(sys.argv[1:])
