#!/bin/bash
mkdir -p /data/db
mongod &
/usr/bin/python3 /app/app.py &
cron -f &
/usr/bin/python3 /app/reader.py
