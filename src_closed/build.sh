TEMPLATE_DIR=./templates
STATIC_DIR=./static
BUILD_DIR=../build

# clean build
mkdir -p $BUILD_DIR
rm -Rf $BUILD_DIR/*

# generate html
for tpl in index 
  do
    cat $TEMPLATE_DIR/header.tpl $TEMPLATE_DIR/$tpl.tpl $TEMPLATE_DIR/footer.tpl > $BUILD_DIR/$tpl.html
done

# copy static
for fic in $STATIC_DIR/*
  do
    cp -Rp $fic $BUILD_DIR/
done
