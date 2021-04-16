#!/bin/bash

echo "remove result"
rm -r result/
echo "remove build"
rm -r build/
echo "remove dist"
rm -r dist/
echo "remove *.egg-info"
rm -r *.egg-info/

pip3 uninstall pyoffice