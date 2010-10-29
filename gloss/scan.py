import parser
import token
import symbol
import sys

def get_file_trans_strings(file_path):
    src = open(file_path, 'rb').read()
    tree = parser.st2list(parser.suite(src))
    return [x for x in walk_for_trans(tree) if x]

def walk_for_trans(level):
    if len(level) == 3 and \
    level[:2] == [symbol.power, [symbol.atom, [token.NAME, '_']]]:
        yield find_string(level[2])

    for l in level:
        if type(l) is list:
            for i in walk_for_trans(l):
                yield i

def find_string(level):
    if level[:1] == [token.STRING]:
        return eval(level[1]).decode('utf-8').strip()

    for l in level:
        if type(l) is list:
            s = find_string(l)
            if s:
                return s
