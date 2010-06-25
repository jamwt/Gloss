from gloss.fs import get_x_yaml_files
from gloss.strutil import locale_from_fn
import yaml
from thread import get_ident
from contextlib import contextmanager
from collections import defaultdict

current_catalog = None
default_locale = None
thread_contexts = defaultdict(list)

def load_gloss_catalog(d, def_locale='en_US'):
    global default_locale 
    global current_catalog
    current_catalog = defaultdict(dict)
    for f in get_x_yaml_files(d):
        locale_n = locale_from_fn(f)
        d = yaml.load(open(f, 'rb').read())
        if type(d) is dict:
            current_catalog[locale_n] = d
    default_locale = current_catalog[def_locale]

def get_translation(s):
    assert current_catalog, "No catalog loaded; use load() first"
    tid = get_ident()
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
    tid = get_ident()
    thread_contexts[tid].append(l)
    yield
    thread_contexts[tid].pop()
