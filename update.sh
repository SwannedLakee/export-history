#!/bin/bash
cd "$(dirname "$0")"
python3 export_history.py
rm *-shm *-wal
