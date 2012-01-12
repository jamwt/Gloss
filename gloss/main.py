from gloss.fs import get_all_py_files, get_x_txt_files
from gloss.scan import get_file_trans_strings
from gloss.output import Task
from gloss.strutil import locale_from_fn
from gloss.serial import dict_to_locale, locale_to_dict
import traceback
import os

def build_catalog(source_d, x_dir, remove_stale=False):

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

    j = Task("Loading locale translations from %s/*.txt" % x_dir)

    fs = get_x_txt_files(x_dir)
    locales = {}
    for f in fs:
        j.subtask(f)
        try:
            d = locale_to_dict(f)
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

        if remove_stale:
            for s in xs.keys():
                if s not in strings:
                    del xs[s]

    Task.line()
    j = Task("Saving updated translation catalogs")

    for n, xs in locales.iteritems():
        j.subtask('%s -> %s' % (locale_from_fn(n), n))
        dict_to_locale(n, xs)
        j.st_okay()

    Task.line()
    Task.info("         ~~~~~~~~~~~~~~~~~~~~ DONE ~~~~~~~~~~~~~~~~~~~~")


def cli():
    # --eventually.. get optparse involved
    import sys
    args = sys.argv[1:]
    if len(args) < 2 or len(args) > 3 or \
           len(args) == 3 and args[2] != '--remove-stale':
        sys.stderr.write("error: at least two arguments are required\nusage: gloss source_dir catalog_dir [--remove-stale]\n")
        raise SystemExit(1)

    build_catalog(args[0], args[1], len(args) == 3)

if __name__ == '__main__':
    build_catalog('.', 'trans')
