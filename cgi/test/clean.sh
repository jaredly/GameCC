echo "drop database $3;create database $3;drop database $4;create database $4"|mysql -u"$1" -p"$2"
rm -f `dirname $0`/../../raw_images/*
