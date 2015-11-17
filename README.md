Domogik website sources
=======================

Sources of the domogik official website.

You want to **help us to translate the website** ? Just go on https://www.transifex.com/domogik/domogik-website/ and login with your GitHub account ;)

Prerequisites
=============

You need to install the following packages.

```
pip install staticjinja
```


i18n
====

Refresh locale catalog
----------------------

When the website content has been changd/completed, you can run the script **src/build_i18n_catalog.sh** to upgrade the existing catalog. Commit and push the file.

Then, a few hours later, the new file content will be pulled by Transifex (it is done once a day) and translators will be able to work on translations :)

But **be caution** ! This is the **i18n_website_template.pot** file of the **develop** branch which is used by transifex!. This is done because we want to be able to translate a website before moving it in production! So we need to do translations on the develop branch.

Complete the translations
-------------------------

For this project, the basis language is french, so French is the reference for translations.

If you plan to help us, just go https://www.transifex.com/domogik/domogik-website/ and help us to translate ;). You can login with your Github account!

Add a new language
------------------

You need to upgrade the below files :

* src/index.html and src/404.html : the if clause
* src/build_i18n_catalog.sh : LANG
* src/build.py : LANG

Then Launch the script **src/build_i18n_catalog.sh** to build the new language catalogs.

Build the website
=================

Just go in **src** and  :

* run the **build.py** script to get the last translations
* run the **build.py** script to build the website

Example : 
```
cd ./src/
./build_transifex_translations.sh
./build.py
```

The built website is located in the **./build/** folder.
