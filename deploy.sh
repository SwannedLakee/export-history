#!/bin/bash
cd "$(dirname "$0")"
python3 export_history.py
cat head.html > index.html
cat history.html >> index.html
git commit -a -m "Update"
git push 
