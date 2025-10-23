from flask import Flask, request, jsonify
import json
import os
import sqlite3

app = Flask(__name__)

# JSON and SQLite paths
JSON_DB = 'database.json'
SQL_DB = 'users.db'

# Save account in readable JSON
def save_to_json(email, password):
    data = []
    if os.path.exists(JSON_DB):
        with open(JSON_DB, 'r') as f:
            data = json.load(f)
    data.append({'email': email, 'password': password})
    with open(JSON_DB, 'w') as f:
        json.dump(data, f, indent=2)

# Create SQLite DB and migrate users
def migrate_to_sqlite():
    if not os.path.exists(JSON_DB):
        return  # Nothing to migrate
    conn = sqlite3.connect(SQL_DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Read users from JSON and insert into SQLite
    with open(JSON_DB, 'r') as f:
        users = json.load(f)
    for u in users:
        try:
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (u['email'], u['password']))
        except sqlite3.IntegrityError:
            pass  # skip duplicates
    conn.commit()
    conn.close()
    os.remove(JSON_DB)  # remove JSON after migration
    print("Migration complete: JSON -> SQLite")

# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    if os.path.exists(SQL_DB):
        # Save to SQLite
        conn = sqlite3.connect(SQL_DB)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'User already exists'}), 400
        conn.close()
        return jsonify({'message': 'Account created in SQLite'}), 200
    else:
        # Save to JSON
        save_to_json(email, password)
        # First account triggers migration
        with open(JSON_DB, 'r') as f:
            if len(json.load(f)) == 1:
                migrate_to_sqlite()
        return jsonify({'message': 'Account created in JSON'}), 200

# Health check endpoint
@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

if __name__ == '__main__':
    # Render expects port 10000
    app.run(host='0.0.0.0', port=10000)
