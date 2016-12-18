LOCALE_DIR=./locale/
DOMAIN=website
#LANGUAGES="fr_FR en_US it_IT"
LANGUAGES="fr en it ru"


# extract all things to translate from the templates
echo "==== i18n : extract the catalog ===="
pybabel extract --mapping babel.cfg --output i18n_website_template.pot ./

### below is commented because it is needed only if we would not use transifex !!!!

# # create or upgrade the catalogs
# for lang in $LANGUAGES
#   do
#     echo "==== i18n : $lang ===="
#     if [ -f ./locale/$lang/LC_MESSAGES/$DOMAIN.po ] ; then
#         echo "The catalog already exists : upgrading it..."
#         pybabel update --input-file i18n_website_template.pot --output-dir $LOCALE_DIR --locale $lang --domain $DOMAIN
#     else
#         echo "The catalog does not exists : creating it..."
#         pybabel init --input-file i18n_website_template.pot --output-dir $LOCALE_DIR --locale $lang --domain $DOMAIN
#     fi
# done


# # build the caalogs
# echo "==== i18n : build the catalogs ===="
# pybabel compile -f --directory $LOCALE_DIR --domain $DOMAIN

