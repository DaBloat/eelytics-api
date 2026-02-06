#!/bin/bash
cp accounts.db account_back.db

sqlite3 account_back.db .dump > sql_dump.sql

sqlite3 accounts.db < sql_dump.sql

rm -rf sql_dump.sql account_back.db
