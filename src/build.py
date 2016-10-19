#!/usr/bin/python
# -*- coding: utf-8 -*-


from staticjinja import make_site
from csscompressor import compress

import jinja2
import gettext
import os
import shutil
import re
import sys

URL="http://www.domogik.org"
OUT_DIR = "../build/"
LOCALE_DIR = "./locale/"
STATIC_DIR = "./static/"
ROOT_FILES = ["./index.html", "404.html", ".htaccess", "robots.txt"]    #, "sitemap.xml"]
TEMPLATES_DIR = "./templates/"
BLOG_DIR_PREFIX = "./blog"
SCREENSHOTS_DIR = "./screenshots"
IMAGES_DIR = "./images"
BLOG_URL_PREFIX = "./"
SITEMAP_TEMPLATE = "./sitemap.xml"

LANG = ["fr", "en"]
LANG_READMORE = {"fr" : "Lire plus...", 
                 "en" : "Read more..."}
LANG_SCREENSHOT = {"fr" : "Capture d'ecran de Domogik",
                   "en" : "Domogik screenshot"}
LANG_IMAGES = {"fr" : "Domogik, pour connecter votre maison.",
                   "en" : "Domogik, your connected house."}





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
            url = os.path.join("{0}".format(BLOG_URL_PREFIX), fic)
            header = ""
            content = ""
            thumbnail = u"none.jpg"
            title = u"No title found !"
            # read the file to grab data
            with open(os.path.join(mypath, fic)) as f:
                in_header = True
                for line in f:
                    #print(line)

                    # find title
                    m = re.match(".*<h1>(.*)</h1>.*", line)
                    if m:
                        title = unicode(m.group(1), "utf8")

                    # find thumbnail
                    m = re.match(".*<!-- *thumbnail *: *(.*)-->.*", line)
                    if m:
                        thumbnail = m.group(1)

                    # find end of header
                    if line.strip() == "<!-- stop -->":
                        in_header = False
                        #print("--Fin du header")
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
    data.sort()
    data.reverse()
    return data


def get_screenshots():
    """
    Sample : 
    return [{"file" : "file1.jpg"}, {"file" : "file2.jpg"}, ...]
    """
    mypath = os.path.join(STATIC_DIR, SCREENSHOTS_DIR)
    data = []
    for fic in os.listdir(mypath):
        # TODO : improve this line
        if os.path.isfile(os.path.join(mypath, fic)) and fic[-4:] in ['.jpg', '.png', '.gif']:
            data.append({"file" : fic})
    return data


def get_static_images():
    """
    Sample : 
    return [{"file" : "file1.jpg"}, {"file" : "file2.jpg"}, ...]
    """
    mypath = os.path.join(STATIC_DIR, IMAGES_DIR)
    data = []
    for fic in os.listdir(mypath):
        # TODO : improve this line
        if os.path.isfile(os.path.join(mypath, fic)) and fic[-4:] in ['.jpg', '.png', '.gif']:
            data.append({"file" : fic})
    return data


def build_sitemap(lang, screenschots, images):
    """ Build the sitemap.xml
    """
    ### include the screenshots and images
    screenshot_data = ""
    image_data = ""
    for screen in screenshots:
        screenshot_data += """
  <image:image>
    <image:loc>{0}/{1}/screenshots/{2}</image:loc>
    <image:caption>{3}</image:caption>
    <image:title>{3}</image:title>
  </image:image>  
""".format(URL, lang, screen['file'], LANG_SCREENSHOT[lang])

    for image in images:
        image_data += """
  <image:image>
    <image:loc>{0}/{1}/images/{2}</image:loc>
    <image:caption>{3}</image:caption>
    <image:title>{3}</image:title>
  </image:image>  
""".format(URL, lang, image['file'], LANG_IMAGES[lang])


    pattern_screenshots_tag = re.compile("^.*<!-- SCREENSHOTS -->.*$")
    pattern_images_tag = re.compile("^.*<!-- IMAGES -->.*$")

    fic = open(SITEMAP_TEMPLATE)
    new_sitemap = ""
    for line in fic:
        new_line = line
        if pattern_screenshots_tag.match(new_line):
            new_line += screenshot_data
        elif pattern_images_tag.match(new_line):
            new_line += image_data
        new_sitemap += new_line
    fic.close()

    fic = open("{0}/sitemap.xml".format(OUT_DIR), "w")
    fic.write(new_sitemap)
    fic.close()

if __name__ == "__main__":


    ### language independant files
    for fic in ROOT_FILES:
        shutil.copy(fic, OUT_DIR)

    ### list screenshots (used bu the screenshot page  and static images (used by the index)
    screenshots = get_screenshots()
    static_images = get_static_images()

    ### build sitemap
    # yes, for now there is only one sitemap referenced on google side...
    # TODO : handle multilangual sitemaps in this script and in google console
    build_sitemap("fr", screenshots, static_images)


    ### langauge specific
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

        ### list blog files
        # notice that we assume that the blog entries can be different between each language, so they are not translated over transifex !
        blog_headers = get_blog_headers(lang)


        ### build website 
        site = make_site(contexts = [('index.html',  {'blog_headers' : blog_headers}),
                                     ('blog.html',  {'blog_headers' : blog_headers}),
                                     ('screenshots.html',  {'screenshots' : screenshots})],
                         outpath = dir,
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)

        site.render()


        ### build blog entries
        blog_dir = "./{0}-{1}".format(BLOG_DIR_PREFIX, lang)
        # copy the layout file in the blog source folder
        shutil.copy(os.path.join(TEMPLATES_DIR, "layout.html"), blog_dir)
        ##"""
        ##os.mkdir(os.path.join(dir, blog_dir))
        ##
        ### copy static files
        ### yes, we copy them twice... for static part and blog part... May be improved
        ##for fic in os.listdir(STATIC_DIR):
        ##    if os.path.isdir(os.path.join(STATIC_DIR, fic)):
        ##        shutil.copytree(os.path.join(STATIC_DIR, fic), os.path.join(dir, blog_dir, fic))
        ##"""

        site = make_site(searchpath = blog_dir,
                         #outpath = os.path.join(dir, blog_dir),
                         outpath = os.path.join(dir),
                         extensions = ['jinja2.ext.i18n'])
        translations = gettext.translation(domain = "website", localedir = LOCALE_DIR, languages = [lang], codeset = "utf-8")
        site._env.install_gettext_translations(translations)

        site.render()


        ### optimize builded data

        print("Optimizing css...")
        # minify all the css files
        mypath = OUT_DIR
        for root, dirs, files in os.walk(mypath):
            for fic in files:
                fic_path = os.path.join(root, fic)
                if fic[-4:] == ".css":
                    # minify only not already minified files
                    if fic[-8:-4] != ".min":
                        print("- {0}".format(fic_path))
                        with open(fic_path) as f:
                           new_css = compress(f.read())
                        with open(fic_path, "w") as f:
                           f.write(new_css)
                      
