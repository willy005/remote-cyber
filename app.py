import os
import sqlite3
from flask import Flask, render_template_string, request, redirect, g
from datetime import datetime

app = Flask(__name__)

# DATABASE - Uses Postgres if available, else local file
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
    # Render gives postgres:// but psycopg needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    DATABASE = 'cyber.db'

def get_db():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    else:
        conn = sqlite3.connect('cyber.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    db = get_db()
    cur = db.cursor()
    if USE_POSTGRES:
        cur.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id SERIAL PRIMARY KEY, service TEXT, name TEXT, phone TEXT, email TEXT, amount INTEGER, status TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    else:
        cur.execute('''CREATE TABLE IF NOT EXISTS orders 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, service TEXT, name TEXT, phone TEXT, email TEXT, amount INTEGER, status TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    db.commit()
    db.close()

# SERVICES - WITH YOUR NEW SERVICES ADDED
SERVICES = [
    {"id": "kra", "name": "KRA Services", "icon": "📄", "price": 500, "description": "KRA PIN, Filing Returns, Compliance", "delivery": "Same Day"},
    {"id": "passport", "name": "Passport Application", "icon": "✈️", "price": 1500, "description": "New, Renewal, Lost passport help", "delivery": "1 Day"},
    {"id": "epra", "name": "EPRA License", "icon": "⛽", "price": 3000, "description": "Energy licensing assistance", "delivery": "3 Days"},
    {"id": "website-design", "name": "Website Design", "icon": "🎨", "price": 5000, "description": "Professional modern website design - business, portfolio, landing page. Mobile-friendly, fast, with M-Pesa integration.", "delivery": "3 Days"},
    {"id": "website-development", "name": "Website Development", "icon": "💻", "price": 15000, "description": "Full website development - eCommerce, booking system, cyber portal like Cyber Mtaani. Hosting + domain + M-Pesa Till + admin panel included.", "delivery": "7 Days"},
]

# [Keep your HTML template code here as before - I can send full HTML if you need]

@app.route('/')
def home():
    init_db()
    # Your existing home page code
    return "Cyber Mtaani - Website running! DB Connected: " + ("POSTGRES ✅" if USE_POSTGRES else "SQLITE")

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
