import os
def locale_from_fn(fn):
    return os.path.basename(fn).split('.')[0]
