#!/bin/bash
cd "$(dirname "$0")"

echo "We are here in history"
echo "We are here in history">log.txt

python3 export_history.py

rm *-shm *-wal
