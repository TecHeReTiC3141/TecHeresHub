import sqlite3 as sql

with sql.connect('../tmp/sql/users.db') as user_on:
    cur = user_con.cursor()

