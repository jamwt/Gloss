import os

def get_all_py_files(d):
    for dname, sd, fs in os.walk(d):
        for f in fs:
            if f.endswith('.py'):
                yield os.path.join(dname, f)


def get_x_txt_files(d):
    for f in os.listdir(d):
        full = os.path.join(d, f)
        if os.path.isfile(full) and f.endswith('.txt'):
            yield full
