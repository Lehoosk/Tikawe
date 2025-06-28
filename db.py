import sqlite3
from flask import g

#SQL commands
def get_connection():
    "Establishes the connection to database"
    con = sqlite3.connect("database.db", timeout=2)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    "Executes the SQL with given parameters to db"
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def query(sql, params=[]):
    "Executes the SQL query and return the results"
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def last_insert_id():
    "Returns value of the last ID"
    return g.last_insert_id
