#!/bin/bash

echo 'example ./install.sh python3.6 to build with python3.6. Default is python3'
if [[ $1 == '' ]]
then
  pyv=python3
else
  pyv=$1
fi
echo "using python version: "`$pyv -V`
echo "upgrading latest pip"
#$pyv -m pip install -U pip
$pyv -m pip install --use-feature=in-tree-build -v --log build.log .

