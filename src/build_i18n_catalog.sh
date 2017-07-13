LOCALE_DIR=./locale/
DOMAIN=website
#LANGUAGES="fr_FR en_US it_IT"
LANGUAGES="fr en it ru"


# extract all things to translate from the templates
echo "==== i18n : extract the catalog ===="
pybabel extract --mapping babel.cfg --output i18n_website_template.pot ./


