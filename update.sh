#!/bin/bash
cd "$(dirname "$0")"
cd ../todo.txt/
git log | grep "##" > ../history/logs.md 
cd -
python3 export_history.py
cp history.html spare.html

rm *-shm *-wal
