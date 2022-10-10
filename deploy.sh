#!/bin/bash
cd "$(dirname "$0")"
cp /Users/joe/Library/Application\ Support/Firefox/Profiles/er7tx3r3.default-release/places.sqlite databases/firefox.sqlite
python3 export_history.py 
cat head.html > index.html
cat history.html >> index.html
git commit -a -m "Update"
git push 
