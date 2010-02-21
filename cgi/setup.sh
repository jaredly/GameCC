# stuff to do: add 127.0.1.2 gamecc.local to /etc/hosts
# add that stuff to /etc/apache2/sites-available

# install python-mysqldb
echo "create user '$1'@'localhost' identified by '$2';grant all on *.* to '$1'@'localhost';create database $3;create database $4;"|mysql -uroot -p

