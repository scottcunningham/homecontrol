#!/bin/bash

host=pi3
src=$(echo $(dirname $0))/..
srcs=$(echo $src/*.py $src/templates $src/static)
initd=etc/init.d/volcontrol
nginxvhost=etc/nginx/sites-enabled/default
installdir=/home/pi/vol

echo 'Deploying script..'
scp -r $srcs pi3:$installdir/
scp -r $initd pi3:/tmp/vol-initd
ssh -t pi3 sudo cp /tmp/vol-initd /etc/init.d/volcontrol
ssh -t pi3 sudo systemctl daemon-reload
scp -r $nginxvhost pi3:/tmp/vol-vhost
ssh -t pi3 sudo cp /tmp/vol-vhost /etc/nginx/sites-enabled/default
ssh -t pi3 sudo serive nginx reload
echo 'Restarting service..'
ssh -t pi3 sudo service volcontrol restart
echo 'Checking service health..'
ssh -t pi3 sudo service volcontrol status | grep Active
echo 'Done!'
