import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRES = bool(DATABASE_URL)
if USE_POSTGRES and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def get_db():
    if USE_POSTGRES:
        import psycopg2
        return psycopg2.connect(DATABASE_URL)
    else:
        conn = sqlite3.connect('cyber.db')
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    db = get_db()
    cur = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY, service TEXT, name TEXT, phone TEXT,
        amount INTEGER, status TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""" if USE_POSTGRES else """CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT, service TEXT, name TEXT, phone TEXT,
        amount INTEGER, status TEXT, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
    cur.execute(sql)
    db.commit()
    db.close()

SERVICES = [
    {"id": "kra-pin", "name": "KRA Services", "icon": "📄", "price": 500, "desc": "KRA PIN, Filing Returns, Compliance"},
    {"id": "passport", "name": "Passport Application", "icon": "✈️", "price": 1500, "desc": "New, Renewal, Lost passport help"},
    {"id": "epra", "name": "EPRA License", "icon": "⛽", "price": 3000, "desc": "Energy licensing assistance"},
    {"id": "ecitizen", "name": "eCitizen Services", "icon": "🇰🇪", "price": 500, "desc": "Good Conduct, Business Registration"},
    {"id": "website-design", "name": "Website Design", "icon": "🎨", "price": 5000, "desc": "Modern mobile-friendly website design for business, portfolio, church, school. Includes M-Pesa & WhatsApp."},
    {"id": "website-development", "name": "Website Development", "icon": "💻", "price": 15000, "desc": "Full eCommerce, Booking System, Cyber Portal. Hosting + Domain + M-Pesa Till + Admin included."},
]

@app.route('/')
def home():
    try: init_db()
    except: pass
    return render_template('index.html', services=SERVICES, postgres=USE_POSTGRES)

@app.route('/order', methods=['GET','POST'])
def order():
    if request.method == 'GET':
        sid = request.args.get('service','kra-pin')
        svc = next((x for x in SERVICES if x['id']==sid), SERVICES[0])
        return render_template('order.html', service=svc)
    else:
        db = get_db()
        cur = db.cursor()
        data = (request.form.get('service'), request.form.get('name'), request.form.get('phone'), request.form.get('amount'), f"paid:{request.form.get('mpesa_code')}")
        if USE_POSTGRES:
            cur.execute("INSERT INTO orders (service,name,phone,amount,status) VALUES (%s,%s,%s,%s,%s)", data)
        else:
            cur.execute("INSERT INTO orders (service,name,phone,amount,status) VALUES (?,?,?,?,?)", data)
        db.commit()
        db.close()
        return render_template('success.html', name=request.form.get('name'))

@app.route('/favicon.ico')
def favicon(): return "", 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",10000)))
