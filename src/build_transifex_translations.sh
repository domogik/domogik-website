PROJECT=domogik-website
RESOURCE=i18n_website_templatepot   # no dot inside!
LOCALE_DIR=./locale/
DOMAIN=website

LANGS="fr en ru"

echo "Download translations from Transifex..."
echo "Login :"
read LOGIN
echo "Password :"
read PASSWORD
for lang in $LANGS
  do
    echo "- $lang..."
    mkdir -p $LOCALE_DIR/$lang/LC_MESSAGES/
    curl -i -L --user $LOGIN:$PASSWORD -X GET "https://www.transifex.com/api/2/project/$PROJECT/resource/$RESOURCE/translation/$lang/?mode=reviewed&file" > $LOCALE_DIR/$lang/LC_MESSAGES/website.po
done

echo ""
echo "Check if there was an issue during authentication..."
grep 401 locale/*/LC_MESSAGES/*
if [[ $? -eq 0 ]] ; then
    echo "ERROR : you have used a bad login/password"
    echo "Exiting..."
    exit 1
else
    echo "... ok"
fi
echo "...done"

# build the catalogs
echo ""
echo "Build the translations"
echo "==== i18n : build the catalogs ===="
pybabel compile -f --directory $LOCALE_DIR --domain $DOMAIN
echo "...done"
