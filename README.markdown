gloss
=====

Gloss is a tool and library for internationalizng software written in
the Python programming language.

How it works
============

Gloss walks a Python project tree, scanning every .py file for instances
of `_("String here")`.  It builds a set of all strings inside this function
call and writes them out to a series of text files, one for each locale.

At runtime, the `_` function is imported from gloss, and the translations
can be used from the currently loaded catalog.

Usage
=====

The `gloss` command line tool
-----------------------------

`gloss` takes two arguments:

    gloss project_dir translations_dir
    
 * `project_dir` is the base of your project tree, containing all the .py files that
   contain `_(..)` calls
 * `translations_dir` is a directory that contains a set of <locale>.txt files.  Each
   file is a dictionary of mappings between the string passed to `_(..)` and the
   locale-specific translation of that string

To initialize a new locale, create an empty .txt file; it will be included in the
list of locales to synchronize with the current set of strings:

    $ touch i18n/en_US.txt
    $ gloss src i18n

The file will contain something like this:

    ================================================================================
    goodbye
    ~~~~~~~~~~~~~~~~

    ================================================================================
    hello
    ~~~~~~~~~~~~~~~~


To provide a translation, simply populate the section below the divider,
like so:

    
    ================================================================================
    goodbye
    ~~~~~~~~~~~~~~~~
    cya

    ================================================================================
    hello
    ~~~~~~~~~~~~~~~~
    howdy


The gloss library
-----------------

The gloss library contains 3 functions to integrate translations into your
python program:

 * load_gloss_catalog(dir, default_locale="en_US") -- Load all locale files 
   out of `dir` for translations in the current application.  This function must
   be called before any other gloss functions.
 * _(string) -- Translate the given string using current catalog rules (see below)
 * lang(locale_name) -- Context manager to set the current locale for all code
   contained in the block (see below)

Establishing the current locale using `lang(..)`
------------------------------------------------

`lang(..)` is a context manager, so we use it with the `with` statement:

    with lang("cn_CN"):
        print _("Hello there")

The current locale is thread-local, so use of `lang` in a multi-processing app
is threadsafe.

Catalog rules
-------------

When any string is translated `_(..)` the translation rules are as follows:

 1. If there is a thread-current locale, established with `lang(..)`, and that
    locale contains a non-empty translation, use it
 2. If the `default_locale` contains a non-empty translation, use it
 3. Return the passed string unmodified

These rules ensure these outcomes:

 * You do not have to actually bother with default_locale if your argument strings
   are in that locale--step 2 will be bypassed if that locale is missing from
   the catalog
 * `_(..)` cannot fail

Author
======

Gloss was written by Jamie Turner <jamie@bu.mp> and other developers at
Bump Technologies, Inc.
