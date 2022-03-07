#!/bin/bash
apt-get update
apt-get install nginx -y
rm /etc/nginx/sites-available/default
cp ./default.nginx /etc/nginx/sites-available/default
rm -r /var/www/html
#mkdir web_static
chown linaro:linaro -R web_static
ln -s /home/linaro/web_static /var/www/html

