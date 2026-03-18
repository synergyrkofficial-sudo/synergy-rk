import os
import sqlite3
import random
import string
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)

# --- THE CORS FIX ---
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://synergyrkofficial.com",
            "https://www.synergyrkofficial.com",
            "https://synergy-rk-official.vercel.app",
            "http://localhost:3000",
            "http://127.0.0.1:5500"
        ]
    }
})

# --- DATABASE ---
DB_PATH = "synergy.db"

def _ensure_schema():
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

_ensure_schema()

# --- ROUTES ---

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Synergy RK Backend is LIVE"}), 200

@app.route('/api/stats', methods=['GET'])
def get_status():
    return jsonify({"status": "online"}), 200

@app.route('/api/book', methods=['POST'])
def create_booking():
    data = request.json or {}
    tracking = "SRK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO bookings (tracking_code, customer_name, customer_email, booking_details, created_at) VALUES (?, ?, ?, ?, ?)",
                (tracking, data.get('name'), data.get('email'), data.get('details'), datetime.now(timezone.utc).isoformat())
            )
        
        # Twilio Notification (Optional: Only if ENV vars are set)
        sid = os.getenv('TWILIO_ACCOUNT_SID')
        token = os.getenv('TWILIO_AUTH_TOKEN')
        if sid and token:
            client = Client(sid, token)
            client.messages.create(
                from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_FROM')}",
                body=f"🚀 New Booking: {tracking}\nFrom: {data.get('name')}",
                to=f"whatsapp:{os.getenv('MY_WHATSAPP_NUMBER')}"
            )

        return jsonify({"success": True, "tracking_code": tracking}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)