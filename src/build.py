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
TWITTER_ACCOUNT="@domogik"
TWITTER_CARD_IMAGE="{0}/fr/images/twitter_card_default.jpg".format(URL)

OUT_DIR = "../build/"
LOCALE_DIR = "./locale/"
STATIC_DIR = "./static/"
ROOT_FILES = ["./index.html", "404.html", ".htaccess", "robots.txt", "googlee103ab25fee2af3d.html"]    #, "sitemap.xml"]
TEMPLATES_DIR = "./templates/"
BLOG_DIR_PREFIX = "./blog"
SCREENSHOTS_DIR = "./screenshots"
IMAGES_DIR = "./images"
BLOG_URL_PREFIX = "./"
SITEMAP_TEMPLATE = "./sitemap.xml"

LANG = ["fr", "en", "ru"]
#LANG_READMORE = {"fr" : u"Lire plus...", 
#                 "en" : u"Read more...",
#                 "ru_RU" : u"Read more..."}
#LANG_PUBLISHED = {"fr" : u"Publié le ",
#                  "en" : u"Published on ",
#                  "ru_RU" : u"Published on "}
LANG_SCREENSHOT = {"fr" : u"Capture d'écran de Domogik",
                   "en" : u"Domogik screenshot",
                   "ru" : u"Domogik screenshot"}
LANG_IMAGES = {"fr" : u"Domogik, pour connecter votre maison.",
                   "en" : u"Domogik, your connected house.",
                   "ru" : u"Domogik, your connected house."}





def get_blog_headers(lang):
    """
    Sample : 
    return [{"title" : "titre1", "header" : "fooo", "url" : "url1", "date" : "YYYY-MM-DD"},
            {"title" : "titre2", "header" : "bbbaaarr", "url" : "url2", "date" : "YYYY-MM-DD"}]
    """
    mypath = "{0}-{1}".format(BLOG_DIR_PREFIX, lang)
    data = []
    for fic in os.listdir(mypath):
        # TODO : improve this line
        if os.path.isfile(os.path.join(mypath, fic)) and fic[-5:] == ".html" and fic != "layout.html" and fic != "blog-layout.html":
            url = os.path.join("{0}".format(BLOG_URL_PREFIX), fic)
            header = u""
            content = u""

            # extract publication date
            if fic.startswith("20"):    # if it starts by 20.. it is a year, so a date :) 2017-04-01 for example
                date_pub = fic[0:10]
            else:
                date_pub = None


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
                        m3 = re.match(" *{%- *endblock ", line)
                        m4 = re.match(".*<h1>(.*)</h1>.*", line)
                        m5 = re.match(" *<meta ", line)
                        if not m1 and not m2 and not m3 and not m4 and not m5:
                            header += unicode(line, "utf8")
                    content += unicode(line, "utf8")

            # add the publication date information
            #if date_pub != None:
            #    header += u"<p>{0}<time datetime='{1}'>{1}</time></p>".format(LANG_PUBLISHED[lang], date_pub)

            # add the 'read more' link
            #header += "<a href='{0}'>{1}</a>".format(url, LANG_READMORE[lang])

            # replace the title by a link
            header = header.replace("<h1>", "<h1><a href='{0}'>".format(url))
            header = header.replace("</h1>", "</a></h1>")

            data.append({"title" : title,
                         "thumbnail" : thumbnail,
                         "url" : url,
                         "header" : header,
                         "date_pub" : date_pub,
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
            # don't process icons and background
            if fic.startswith("icon"):
                pass
            elif fic.startswith("background"):
                pass
            else:
                data.append({"file" : fic})
    return data


def build_sitemap(lang, screenschots, images):
    """ Build the sitemap.xml
    """
    ### include the screenshots and images
    screenshot_data = ""
    image_data = ""
    for screen in screenshots:
        screenshot_data += u"""
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
    new_sitemap = u""
    for line in fic:
        new_line = u"{0}".format(line)
        if pattern_screenshots_tag.match(new_line):
            new_line += screenshot_data
        elif pattern_images_tag.match(new_line):
            new_line += image_data
        new_sitemap += new_line
    fic.close()

    fic = open("{0}/sitemap.xml".format(OUT_DIR), "w")
    fic.write(new_sitemap.encode('UTF-8'))
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


    context_meta_twitter = {
                              'url' : URL,
                              'twitter_account' : TWITTER_ACCOUNT,
                              'twitter_card_image' : TWITTER_CARD_IMAGE
                           }
    ### language specific
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
        context_index = {'blog_headers' : blog_headers}
        context_blog = {'blog_headers' : blog_headers}
        context_screenshots = {'screenshots' : screenshots}
        context_index.update(context_meta_twitter)
        context_blog.update(context_meta_twitter)
        context_screenshots.update(context_meta_twitter)

        site = make_site(contexts = [('index.html',  context_index),
                                     ('blog.html',  context_blog),
                                     ('screenshots.html',  context_screenshots)],
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
                         extensions = ['jinja2.ext.i18n'],
                         contexts = [('.*.html', context_meta_twitter)]
                         )
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
                      
