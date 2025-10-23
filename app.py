from flask import Flask, request, jsonify
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
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    # Save to JSON
    save_to_json(email, password)
    return jsonify({'message': 'Account created in JSON'}), 200

# Health check endpoint
@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

if __name__ == '__main__':
    # Render expects port 10000
    app.run(host='0.0.0.0', port=10000)