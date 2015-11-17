#!/usr/bin/python

from staticjinja import make_site
import jinja2
import gettext
import os
import shutil

OUT_DIR = "../build/"
LOCALE_DIR = "./locale/"
STATIC_DIR = "./static/"
ROOT_FILES = ["./index.html", "404.html", ".htaccess"]

LANG = ["fr", "en"]

if __name__ == "__main__":
    for lang in LANG:
        # define root folder for the lang
        dir = os.path.join(OUT_DIR, lang)
        if not os.path.exists(dir):
            os.makedirs(dir)

        # clean root folder for the lang
        shutil.rmtree(dir)

        # copy static files
        shutil.copytree(STATIC_DIR, dir)
        for fic in ROOT_FILES:
            shutil.copy(fic, OUT_DIR)

        # build website
        site = make_site(outpath = dir,
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)
        site.render()
