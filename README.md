Domogik website sources
=======================

Sources of the domogik official website

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

When the website content has been changd/completed, you can run the script **src/build_i18n_catalog.sh** to upgrade the existing catalog.

Complete the translations
-------------------------

For this project, the basis language is french, so French is the reference for translations.

If you plan to help us, just go in **src/locale/THE_LANGUAGE_YOU_PLAN_TO_CONTRIBUTE_ON/LC_MESSAGES/** and fill the **website.po** file.

Add a new language
------------------

You need to upgrade the below files :

* src/index.html and src/404.html : the if clause
* src/build_i18n_catalog.sh : LANG
* src/build.py : LANG

Then Launch the script **src/build_i18n_catalog.sh** to build the new language catalogs.

Build the website
=================

Just go in **src** and run the **build.py** script : 

```
cd ./src/
./build.py
```

The built website is located in the **./build/** folder.
