# stuff to do: add 127.0.1.2 gamecc.local to /etc/hosts
# add that stuff to /etc/apache2/sites-available

# install python-mysqldb
echo "create user 'gameccadmin'@'localhost' identified by 'aWdX=';grant all on *.* to 'gameccadmin'@'localhost';create database gameccblog;create database gameccdata;"|mysql -uroot -p

