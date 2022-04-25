#!/bin/bash
cd "$(dirname "$0")"
cp /Users/joe2021/Library/Application\ Support/Firefox/Profiles/dato3gap.default-release/places.sqlite databases/firefox.sqlite
python3 export_history.py 
cat head.html > index.html
cat socialhead.html > smartsocial.html
cat history.html >> index.html
cat social.html >> smartsocial.html
git commit -a -m "Update"
git push 
