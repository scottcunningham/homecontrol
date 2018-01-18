#!/bin/bash

host=orangepizero
src=$(echo $(dirname $0))/..
srcs=$(echo $src/*.py $src/templates $src/static $src/conf)
initd=etc/init.d/volcontrol
nginxvhost=etc/nginx/sites-enabled/default
installdir=/home/scott/vol

echo 'Deploying script..'
ssh -t $host mkdir $installdir
ssh -t $host mkdir $installdir/logs
scp -r $srcs $host:$installdir/
scp -r $initd $host:/tmp/vol-initd
ssh -t $host sudo cp /tmp/vol-initd /etc/init.d/volcontrol
ssh -t $host sudo systemctl daemon-reload
scp -r $nginxvhost $host:/tmp/vol-vhost
ssh -t $host sudo cp /tmp/vol-vhost /etc/nginx/sites-enabled/default
ssh -t $host sudo service nginx reload
echo 'Restarting service..'
ssh -t $host sudo service volcontrol restart
echo 'Checking service health..'
ssh -t $host sudo service volcontrol status | grep -i active
echo 'Done!'
