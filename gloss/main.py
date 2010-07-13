from gloss.fs import get_all_py_files, get_x_yaml_files, save_file
from gloss.scan import get_file_trans_strings
from gloss.output import Task
from gloss.strutil import locale_from_fn
import yaml
import traceback
import os

def build_catalog(source_d, x_dir):

    j = Task("Scanning .py files for translation strings")
    fs = get_all_py_files(source_d)
    strings = set()
    for f in fs:
        j.subtask(f)
        try:
            strings.update(get_file_trans_strings(f))
        except:
            j.st_fail(traceback.format_exc())
        else:
            j.st_okay()
    Task.info("Strings found: %s" % len(strings))

    j = Task("Loading locale translations from %s/*.yaml" % x_dir)
    
    fs = get_x_yaml_files(x_dir)
    locales = {}
    for f in fs:
        j.subtask(f)
        try:
            d = yaml.load(open(f, 'rb').read())
            if d == '' or d == None:
                d = {}
            assert type(d) is dict
        except:
            j.st_fail(traceback.format_exc())
        else:
            j.st_okay()
            locales[f] = d
            
    Task.line()
    j = Task("Merging translation strings")

    for n, xs in locales.iteritems():
        j.subtask(locale_from_fn(n))
        s_len = len(xs)
        have = 0
        new = 0
        are_set = 0
        for s in strings:
            if s in xs:
                if xs[s]:
                    are_set += 1
                have += 1
            else:
                new += 1
                xs[s] = ''
        j.st_okay()
        j.info('         new=%s, stale=%s, missing=%s' % (new, s_len - have, new + have - are_set), clear=False)

    Task.line()
    j = Task("Saving updated translation catalogs")

    for n, xs in locales.iteritems():
        j.subtask('%s -> %s' % (locale_from_fn(n), n))
        out = yaml.dump(dict((k.encode('utf-8'), v.encode('utf-8')) for k, v in xs.iteritems()), 
        default_flow_style=False, default_style='|', allow_unicode=True)
        save_file(n, out)
        j.st_okay()

    Task.line()
    Task.info("         ~~~~~~~~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~~~~~~~~")


def cli():
    # --eventually.. get optparse involved
    import sys
    args = sys.argv[1:]
    if len(args) != 2:
        sys.stderr.write("error: exactly two arguments are required\nusage: gloss source_dir catalog_dir\n")
        raise SystemExit(1)
    build_catalog(*args)
    
if __name__ == '__main__':
    build_catalog('.', 'trans')
