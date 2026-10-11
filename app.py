from flask import Flask, render_template_string, request, redirect, g
import sqlite3
import datetime
import os

app = Flask(__name__)
DATABASE = 'cyber.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT, service TEXT, amount TEXT,
        status TEXT DEFAULT 'Pending', date TEXT
    )""")
    db.commit()
    db.close()

SERVICES = [
    ("Passport Application", "🛂", "34/50/66 pages", "500"),
    ("EPRA License T1 T2 T3 C1 V1 V2", "⚡", "Avoid fine 5000", "800"),
    ("KRA PIN Registration", "🧾", "New PIN 10 mins", "300"),
    ("KRA Tax Returns", "💰", "Nil & PAYE", "500"),
    ("eCitizen Good Conduct", "🏛️", "Police Clearance", "600"),
    ("Business Registration", "🏢", "Company + Name Search", "1500"),
    ("CV & Cover Letter", "📄", "Professional", "400"),
    ("HELB / NTSA / SHA", "🎓", "Loans & License", "600"),
]

# (Use the full TEMPLATE I gave you before - paste it here)
# For brevity, I'm using a short version - replace with full HTML for production
TEMPLATE = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remote Cyber Services</title>
<style>body{font-family:Arial;margin:0;background:#f4f7fb}.header{background:#0a2a66;color:white;padding:40px 20px;text-align:center}.header h1{color:#ffcc00}.btn{background:#ffcc00;color:#0a2a66;padding:12px 20px;border-radius:25px;text-decoration:none;font-weight:bold;display:inline-block;margin:4px}</style>
</head><body>
<div class="header"><h1>REMOTE CYBER SERVICES</h1><p>0706507594 | FAST RELIABLE REMOTE</p><a class="btn" href="https://wa.me/254706507594">WhatsApp Us</a></div>
<div style="padding:20px;text-align:center"><h2>Website is LIVE on Render!</h2><p>Your site is working.</p></div>
</body></html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE, services=SERVICES)

@app.route('/admin')
def admin():
    return "Admin - orders will show here"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)