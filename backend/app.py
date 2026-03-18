import os
import sqlite3
import random
import string
from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)

# --- 1. THE ABSOLUTE CORS FIX ---
# This allows your official domain and Vercel to talk to this Render backend
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

# --- 2. DATABASE CONFIGURATION ---
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
    print("✅ Database schema verified.")

init_db()

# --- 3. NOTIFICATION LOGIC (TWILIO) ---
def send_whatsapp_notification(tracking, name, details):
    sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN')
    from_whatsapp = os.getenv('TWILIO_WHATSAPP_FROM')
    to_whatsapp = os.getenv('MY_WHATSAPP_NUMBER')

    if all([sid, token, from_whatsapp, to_whatsapp]):
        try:
            client = Client(sid, token)
            message = client.messages.create(
                from_=f"whatsapp:{from_whatsapp}",
                body=f"🚀 *New Synergy RK Booking*\n\n"
                     f"*ID:* {tracking}\n"
                     f"*Client:* {name}\n"
                     f"*Project:* {details}",
                to=f"whatsapp:{to_whatsapp}"
            )
            return True
        except Exception as e:
            print(f"❌ Twilio Error: {e}")
    return False

# --- 4. ROUTES ---

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Synergy RK API is fully functional",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

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
        return jsonify({"error": "Missing required fields"}), 400

    # Generate Unique Tracking Code
    tracking = "SRK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    try:
        # Save to Database
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO bookings (tracking_code, customer_name, customer_email, booking_details, created_at) VALUES (?, ?, ?, ?, ?)",
                (tracking, name, email, details, datetime.now(timezone.utc).isoformat())
            )
        
        # Trigger WhatsApp Notification
        send_whatsapp_notification(tracking, name, details)

        return jsonify({
            "success": True, 
            "tracking_code": tracking,
            "message": "Booking recorded successfully"
        }), 201

    except Exception as e:
        print(f"❌ Database Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    # Use environment port for Render deployment
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)