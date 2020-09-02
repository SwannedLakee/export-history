#!/bin/bash
cd "$(dirname "$0")"
cd ../todo.txt/
git log | grep "##" > ../history/logs.md 
cd -
python export_history.py

rm *-shm *-wal
