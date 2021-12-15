#!/bin/bash
cd "$(dirname "$0")"
python3 export_history.py
copy history.html index.html
git commit -a -m "Update"
git push 
