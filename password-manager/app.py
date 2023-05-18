from flask import Flask, render_template
import sqlite3
import os
from generate_password import generate
from pyperclip import copy

app = Flask(__name__)

con = sqlite3.connect("pwd-mngr.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER AUTO_INCREMENT PRIMARY KEY, email TEXT NOT NULL, hash TEXT NOT NULL, verified NUMBER(0));")

@app.route('/')
def index():
    return render_template('index.html')