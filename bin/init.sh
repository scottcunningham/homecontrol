#!/bin/bash

set -e

host=orangepizero

APT_PKGS="nginx mopidy python{,3}-pip python{,3}-dev python{,3}-setuptools libffi-dev python-spotify"
PIP_PKGS="wheel flask pyhs100 pylgtv"
PIP2_PKGS="wheel mopidy mopidy-spotify Mopidy-Iris mopidy-moped"

# spotify/mopidy stuff
ssh $host "wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -"
ssh $host "sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/jessie.list"

ssh $host sudo apt-get update
ssh $host sudo apt-get install -y ${APT_PKGS}
ssh $host sudo pip3 install ${PIP_PKGS}
ssh $host sudo service mopidy start

ssh $host -t sudo chown mopidy:scott /etc/mopidy/mopidy.conf^C
ssh $host -t sudo chmod 770 /etc/mopidy/mopidy.conf
