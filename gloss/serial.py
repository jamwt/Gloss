import os

T_SEP = '\n' + ('~' * 16) + '\n'
P_SEP = '\n' + ('=' * 80) + '\n'
def dict_to_locale(path, d):
    t_path = path + '.tmp'
    with open(t_path, 'wb') as fd:
        for k, v in sorted(d.items()):
            k = k.encode('utf-8')
            v = v.encode('utf-8')
            assert T_SEP not in k
            assert P_SEP not in k
            assert T_SEP not in v
            assert P_SEP not in v
            fd.write("%s%s%s%s" % (
            P_SEP, k, T_SEP, v))


    os.rename(t_path, path)


def locale_to_dict(path):
    d = {}
    raw = open(path, 'rb').read()
    for block in raw.split(P_SEP):
        if block:
            k, v = map(str.strip, block.split(T_SEP))
            if k:
                d[k.decode('utf-8')] = v.decode('utf-8')

    return d
