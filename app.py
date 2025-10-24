from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# JSON path
JSON_DB = 'database.json'

# Save account in readable JSON
def save_to_json(email, password):
    data = []
    if os.path.exists(JSON_DB):
        with open(JSON_DB, 'r') as f:
            data = json.load(f)
    data.append({'email': email, 'password': password})
    with open(JSON_DB, 'w') as f:
        json.dump(data, f, indent=2)

# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.form  # Use request.form for form data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Save to JSON
    save_to_json(email, password)
    return jsonify({'message': 'Account created in JSON'}), 200

# Serve the login page
@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')  # Serve the login.html template

if __name__ == '__main__':
    # Render expects port 10000
    app.run(host='0.0.0.0', port=10000)