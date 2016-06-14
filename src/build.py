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
BLOG_DIR_PREFIX = "./blog"

LANG = ["fr", "en"]
LANG_READMORE = {"fr" : "Lire plus...", 
                 "en" : "Read more..."}




def get_blog_headers(lang):
    """
    Sample : 
    return [{"title" : "titre1", "header" : "fooo", "url" : "url1"},
            {"title" : "titre2", "header" : "bbbaaarr", "url" : "url2"}]
    """
    mypath = "{0}-{1}".format(BLOG_DIR_PREFIX, lang)
    data = []
    for fic in os.listdir(mypath):
        # TODO : improve this line
        if os.path.isfile(os.path.join(mypath, fic)) and fic[-5:] == ".html" and fic != "layout.html" and fic != "blog-layout.html":
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
                        # filter some jinja templates lines to get the header
                        m1 = re.match(" *{% *(extends|block|endblock)", line)
                        m2 = re.match(" *{% *block ", line)
                        if not m1 and not m2:
                            header += unicode(line, "utf8")
                    content += unicode(line, "utf8")

            # add the 'read more' link
            header += "<a href='{0}'>{1}</a>".format(url, LANG_READMORE[lang])

            # replace the title by a link
            header = header.replace("<h1>", "<h1><a href='{0}'>".format(url))
            header = header.replace("</h1>", "</a></h1>")

            data.append({"title" : title,
                         "thumbnail" : thumbnail,
                         "url" : url,
                         "header" : header,
                         "content" : content})
    data = sorted(data, key=lambda k: k['url'], reverse = True) 
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

        ### list blog files
        # notice that we assume that the blog entries can be different between each language, so they are not translated over transifex !
        blog_headers = get_blog_headers(lang)

        ### build website 
        site = make_site(contexts = [('index.html',  {'blog_headers' : blog_headers}),
                                     ('blog.html',  {'blog_headers' : blog_headers})],
                         outpath = dir,
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)

        site.render()


        ### build blog entries
        blog_dir = "./{0}-{1}".format(BLOG_DIR_PREFIX, lang)
        os.mkdir(os.path.join(dir, blog_dir))
        # copy the layout file in the blog source folder
        shutil.copy(os.path.join(TEMPLATES_DIR, "layout.html"), blog_dir)

        # copy static files
        # yes, we copy them twice... for static part and blog part... May be improved
        for fic in os.listdir(STATIC_DIR):
            if os.path.isdir(os.path.join(STATIC_DIR, fic)):
                shutil.copytree(os.path.join(STATIC_DIR, fic), os.path.join(dir, blog_dir, fic))

        site = make_site(searchpath = blog_dir,
                         outpath = os.path.join(dir, blog_dir),
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)

        site.render()

