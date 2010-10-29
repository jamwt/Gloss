from gloss.fs import get_x_txt_files
from gloss.strutil import locale_from_fn
from gloss.serial import locale_to_dict
from thread import get_ident
from contextlib import contextmanager
from collections import defaultdict

current_catalog = None
default_locale = None
get_thread_id = None
thread_contexts = defaultdict(list)

def load_gloss_catalog(d, def_locale='en_US', use_greenlet=False):
    global default_locale 
    global current_catalog
    global get_thread_id

    if use_greenlet:
        import greenlet
        def greenlet_get_thread():
            return id(greenlet.getcurrent())
        get_thread_id = greenlet_get_thread
    else:
        get_thread_id = get_ident

    current_catalog = defaultdict(dict)
    for f in get_x_txt_files(d):
        locale_n = locale_from_fn(f)
        d = locale_to_dict(f)
        if type(d) is dict:
            current_catalog[locale_n] = d
    default_locale = current_catalog[def_locale]

def get_translation(s):
    assert current_catalog, "No catalog loaded; use load() first"
    tid = get_thread_id()
    if thread_contexts[tid]:
        thread_cat = current_catalog[thread_contexts[tid][-1]]
        if thread_cat.get(s):
            return thread_cat[s]
    if default_locale.get(s):
        return default_locale[s]
    return s

@contextmanager
def lang(l):
    assert current_catalog, "No catalog loaded; use load() first"
    tid = get_thread_id()
    thread_contexts[tid].append(l)
    yield
    thread_contexts[tid].pop()

def get_catalog(locale=None):
    if locale:
        return current_catalog[locale]
    else:
        return current_catalog
