import os
import sqlite3
import random
import string
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# --- THE ABSOLUTE FIX: ALLOW ALL ORIGINS FOR TESTING ---
# This removes the security wall entirely so we can confirm it works
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Synergy RK Backend is LIVE"}), 200

@app.route('/api/stats', methods=['GET'])
def get_status():
    return jsonify({"status": "online"}), 200

@app.route('/api/book', methods=['POST'])
def create_booking():
    # Simple logic to confirm it works
    data = request.json or {}
    return jsonify({"success": True, "tracking_code": "SRK-SUCCESS"}), 201

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)