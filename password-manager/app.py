import sqlite3

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cryptography.fernet import Fernet
from generate_password import generate
from pyperclip import copy
from functools import wraps

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

con = sqlite3.connect("./pwd-mngr.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL);")
cur.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, url TEXT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL, key TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));")
con.commit()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect('/login')

@app.route('/passwords', methods=['GET'])
@login_required
def passwords():
    con = sqlite3.connect("./pwd-mngr.db")
    cur = con.cursor()

    passwords = cur.execute("SELECT * FROM passwords WHERE user_id = {}".format(session["user_id"])).fetchall()
    decrypted_passwords = []

    for p in passwords:
        key = bytes(p[6][2:-1], 'utf8')
        b = bytes(p[5][2:-1], 'utf8')

        g = Fernet(key)
        decrypted = g.decrypt(b)
        decrypted_passwords.append([p[0], p[1], p[2], p[3], p[4], str(decrypted, 'utf8')])

    return render_template('index.html', passwords=decrypted_passwords)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/login', methods=["GET", "POST"])
def login():
    con = sqlite3.connect("./pwd-mngr.db")
    cur = con.cursor()

    session.clear()

    if request.method == "POST":

        if not request.form.get("email"):
            return render_template('login.html', msg="Invalid user")

        elif not request.form.get("password"):
            return render_template('login.html', msg="Invalid password")

        rows = cur.execute("SELECT * FROM users WHERE email = '{}'".format(request.form.get("email")))
        users = rows.fetchall()

        if len(users) < 1:
            return render_template('login.html', msg="User does not exist")
        if not check_password_hash(users[0][2], request.form.get("password")):
            return render_template('login.html', msg="Password is incorrect")

        session["user_id"] = users[0][0]

        con.commit()

        return redirect("/passwords")

    else:
        return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    con = sqlite3.connect("./pwd-mngr.db")
    cur = con.cursor()
    special_characters = "!@#$%&?"
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        conf = request.form.get("confirmation")
        user = cur.execute(f"SELECT * FROM users WHERE email = '{email}'").fetchall()
        if email == "":
            return render_template('register.html', msg="Invalid Email")
        if len(user) > 0:
            return render_template('register.html', msg="User already exists with this email")
        if pwd == "":
            return render_template('register.html', msg="Invalid Password")
        if len(pwd) < 6 or len(pwd) > 30:
            return render_template('register.html', msg="Password must be between 6 and 30 characters")
        upper = False
        special = False
        num = False
        for c in pwd:
            if c.isupper():
                upper = True
            if c in special_characters:
                special = True
            if c.isdigit():
                num = True
        if not upper:
            return render_template('register.html', msg="Password must atleast 1 uppercase character")
        if not num:
            return render_template('register.html', msg="Password must atleast 1 number")
        if not special:
            return render_template('register.html', msg="Password must atleast 1 of the following special characters: !@#$%&?")
        if conf == "":
            return render_template('register.html', msg="Passwords do not match")
        if conf != pwd:
            return render_template('register.html', msg="Passwords do not match")

        hashed = generate_password_hash(pwd)
        cur.execute(f"INSERT INTO users (email, hash) VALUES ('{email}', '{hashed}');")
        con.commit()
        return redirect("/login")
    else:
        return render_template('register.html')

@app.route('/addaccount', methods=['GET', 'POST'])
def add():
    con = sqlite3.connect("./pwd-mngr.db")
    cur = con.cursor()

    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        website = request.form.get("website")

        if email == "":
            return render_template('addaccount.html', msg="Invalid Email")
        if username == "":
            return render_template('addaccount.html', msg="Invalid Username")
        if website == "":
            return render_template('addaccount.html', msg="Invalid website")
        
        accounts = cur.execute(f"SELECT * FROM users WHERE email = '{email}', username = '{username}', website = '{website}'").fetchall()
        if len(accounts > 0):
            return render_template('addaccount.html', msg="This account already exists.")

        pwd = generate()
        id = session["user_id"]

        key = Fernet.generate_key()
        epwd = pwd.encode()
        f = Fernet(key)
        encrypted = f.encrypt(epwd)

        cur.execute(f'INSERT INTO passwords (user_id, url, username, email, hash, key) VALUES ({id}, "{website}", "{username}", "{email}", "{encrypted}", "{key}");')

        con.commit()
        return redirect("/passwords")

    else:
        return render_template('addaccount.html')