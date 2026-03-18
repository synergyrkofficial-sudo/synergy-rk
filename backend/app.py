import os
import sqlite3
import random
import string
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# --- FIX 1: OPEN CORS TO EVERYTHING ---
# This stops the red errors in your browser console
CORS(app, resources={r"/*": {"origins": "*"}})

# --- DATABASE SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "synergy.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tracking_code TEXT UNIQUE,
                customer_name TEXT,
                customer_email TEXT,
                booking_details TEXT,
                created_at TEXT
            )
        """)

init_db()

# --- FIX 2: ADD THE HOME ROUTE ---
@app.route('/')
def home():
    return "<h1>Synergy RK Backend is LIVE</h1><p>Visit /api/stats to check status.</p>", 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({"status": "online"}), 200

@app.route('/api/book', methods=['POST'])
def create_booking():
    data = request.json or {}
    name = data.get('name')
    email = data.get('email')
    details = data.get('details')

    if not name or not email:
        return jsonify({"error": "Missing info"}), 400

    tracking = "SRK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO bookings (tracking_code, customer_name, customer_email, booking_details, created_at) VALUES (?, ?, ?, ?, ?)",
                (tracking, name, email, details, datetime.now(timezone.utc).isoformat())
            )
        return jsonify({"success": True, "tracking_code": tracking}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)