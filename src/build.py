#!/usr/bin/python
# -*- coding: utf-8 -*-


from staticjinja import make_site
import jinja2
import gettext
import os
import shutil
import re

OUT_DIR = "../build/"
LOCALE_DIR = "./locale/"
STATIC_DIR = "./static/"
ROOT_FILES = ["./index.html", "404.html", ".htaccess"]
TEMPLATES_DIR = "./templates/"
BLOG_DIR_PREFIX = "blog"

LANG = ["fr", "en"]




def get_blog_headers(lang):
    """
    Sample : 
    return [{"title" : "titre1", "header" : "fooo", "url" : "url1"},
            {"title" : "titre2", "header" : "bbbaaarr", "url" : "url2"}]
    """
    mypath = "{0}-{1}".format(os.path.join(TEMPLATES_DIR, BLOG_DIR_PREFIX), lang)
    data = []
    for fic in os.listdir(mypath):
        if os.path.isfile(os.path.join(mypath, fic)) and fic[-5:] == ".html":
            url = os.path.join("{0}-{1}".format(BLOG_DIR_PREFIX, lang), fic)
            header = ""
            content = ""
            thumbnail = u"none.jpg"
            title = u"No title found !"
            # read the file to grab data
            with open(os.path.join(mypath, fic)) as f:
                in_header = True
                for line in f:
                    print(line)

                    # find title
                    m = re.match(".*<h1>(.*)</h1>.*", line)
                    if m:
                        title = m.group(1)

                    # find thumbnail
                    m = re.match(".*<!-- *thumbnail *: *(.*)-->.*", line)
                    if m:
                        thumbnail = m.group(1)

                    # find end of header
                    if line.strip() == "<!-- stop -->":
                        in_header = False
                        print("--Fin du header")
                    if in_header:
                        header += unicode(line, "utf8")
                    content += unicode(line, "utf8")

            data.append({"title" : title,
                         "thumbnail" : thumbnail,
                         "url" : url,
                         "header" : header,
                         "content" : content})
    data = sorted(data, key=lambda k: k['url'], reverse = True) 
    print(data)
    return data



if __name__ == "__main__":
    for lang in LANG:
        print("==== Building {0} ====".format(lang))
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

        # list blog files
        # notice that we assume that the blog entries can be different between each language, so they are not translated over transifex !
        blog_headers = get_blog_headers(lang)

        # build website 
        site = make_site(contexts = [('index.html',  {'blog_headers' : blog_headers}),
                                     ('blog.html',  {'blog_headers' : blog_headers})],
                         outpath = dir,
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)

        site.render()


