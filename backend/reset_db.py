import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "synergy.db")

def reset():
    if not os.path.exists(DB_PATH):
        print("❌ Database doesn't exist yet.")
        return

    confirm = input("⚠️ Are you sure you want to DELETE ALL bookings? (y/n): ")
    if confirm.lower() == 'y':
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM bookings")
        # Optional: Reset the ID counter back to 1
        conn.execute("DELETE FROM sqlite_sequence WHERE name='bookings'")
        conn.commit()
        conn.close()
        print("🧹 Database cleared! Synergy RK is fresh and ready.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    reset()