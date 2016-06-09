#!/bin/sh

app="timeside"
dir="diagram"

if [ ! -d $dir ]; then
	mkdir $dir
fi

./manage.py graph_models  -a > $dir/$app-all.dot
./manage.py graph_models $app > $dir/$app.dot

sed -i '/#\ /d' $dir/$app-all.dot
sed -i '/#\ /d' $dir/$app.dot

dot $dir/$app-all.dot -Tpdf -o $dir/$app-all.pdf
dot $dir/$app.dot -Tpdf -o $dir/$app.pdf

rsync -a $dir/ doc.parisson.com:/var/www/files/doc/$app/diagram/
