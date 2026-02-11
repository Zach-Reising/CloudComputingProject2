from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import sqlite3

app = Flask(__name__)

DATABASE_NAME = 'reisinzsdatabase.db'

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# SQLite setup
conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL, password TEXT NOT NULL, email TEXT NOT NULL, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT NOT NULL, city TEXT NOT NULL, state TEXT NOT NULL, zipcode TEXT NOT NULL)''')
conn.commit()
conn.close()

def sqlite3_connect(query: str, fetch_one: bool = False, fetch_all: bool = False):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(query)

    if fetch_one:
        result = c.fetchone()
    elif fetch_all:
        result = c.fetchall()
    else:
        result = None

    conn.commit()
    conn.close()

    return result

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipcode']

    file = request.files['limmerick_file']

    if file:
        filename = f"{username}_Limmerick.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

    query = f"INSERT INTO users (username, password, email, first_name, last_name, address, city, state, zipcode) VALUES ('{username}', '{password}', '{email}', '{first_name}', '{last_name}', '{address}', '{city}', '{state}', '{zipcode}')"
    sqlite3_connect(query)
    return redirect(url_for('profile', username=username))

@app.route('/profile/<username>')
def profile(username):
    query = f"SELECT * FROM users WHERE username='{username}'"
    user = sqlite3_connect(query, fetch_one=True)

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{username}_Limmerick.txt")

    word_count = 0
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
            word_count = len(content.split())
    return render_template('profile.html', user=user, word_count=word_count)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = sqlite3_connect(query, fetch_one=True)
    if user:
        return redirect(url_for('profile', username=username))
    else:
        return "Invalid credentials. Please try again."
    
@app.route('/download/<username>')
def download(username):
    filename = f"{username}_Limmerick.txt"
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
