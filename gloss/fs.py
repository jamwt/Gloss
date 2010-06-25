import os
import yaml

def get_all_py_files(d):
    for dname, sd, fs in os.walk(d):
        for f in fs:
            if f.endswith('.py'):
                yield os.path.join(dname, f)


def get_x_yaml_files(d):
    for f in os.listdir(d):
        full = os.path.join(d, f)
        if os.path.isfile(full) and f.endswith('.yaml'):
            yield full

def save_file(fn, contents):
    t_fn = fn + '.tmp'
    open(t_fn, 'wb').write(contents)
    os.rename(t_fn, fn)
