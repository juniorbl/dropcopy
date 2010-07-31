#!/bin/sh

echo '[unzip the file]'
tar zxf dropcopy-1.0.tar.gz
echo '[install]'
cd dropcopy-1.0/
sudo python setup.py install
echo '[copy conf file to /home]'
mkdir $HOME/.dropcopy
cp dropcopy.conf $HOME/.dropcopy/
