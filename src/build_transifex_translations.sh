LOGIN=fritz.smh@gmail.com
PASSWORD=traduirecestchiant
PROJECT=domogik-website
RESOURCE=i18n_website_templatepot   # no dot inside!
LOCALE_DIR=./locale/
DOMAIN=website

LANGS="fr en"

echo "Download translations from Transifex..."
for lang in $LANGS
  do
    echo "- $lang..."
    mkdir -p $LOCALE_DIR/$lang/LC_MESSAGES/
    curl -i -L --user $LOGIN:$PASSWORD -X GET "https://www.transifex.com/api/2/project/$PROJECT/resource/$RESOURCE/translation/$lang/?mode=reviewed&file" > $LOCALE_DIR/$lang/LC_MESSAGES/website.po
done

echo "Done!"

# build the catalogs
echo ""
echo "Build the translations"
echo "==== i18n : build the catalogs ===="
pybabel compile -f --directory $LOCALE_DIR --domain $DOMAIN
