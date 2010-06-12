#!/bin/sh

echo '[unzip the file]'
tar zxf dropcopy-1.0.tar.gz
echo '[install]'
cd dropcopy-1.0/
sudo python setup.py install
cd $HOME
chmod 777 -R $HOME/.dropcopy
