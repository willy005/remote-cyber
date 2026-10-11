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
    ("Passport Application", "🛂", "New, Renewal, Lost - 34/50/66 pages", "500"),
    ("EPRA License T1 T2 T3 C1", "⚡", "Avoid 5K fine - Electrician & Solar", "800"),
    ("KRA PIN Registration", "🧾", "Get KRA PIN in 10 Minutes", "300"),
    ("KRA Tax Returns", "💰", "Nil Returns, PAYE, Turnover Tax", "500"),
    ("Good Conduct (DCI)", "🏛️", "eCitizen Police Clearance", "600"),
    ("Business Registration", "🏢", "Company, Business Name Search", "1500"),
    ("CV & Cover Letter", "📄", "Professional Modern CV + ATS", "400"),
    ("HELB / NTSA / SHA / eCitizen", "🎓", "Compliance & Applications", "600"),
]

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cyber Mtaani - Remote Cyber Services Kenya | 0706507594</title>
<meta name="description" content="Fast Remote Cyber Services in Kenya - Passport, KRA, EPRA, Good Conduct. WhatsApp 0706507594">
<style>
*{margin:0;padding:0;box-sizing:border-box} body{font-family: 'Segoe UI', Arial; background:#f5f7fb; color:#222}
.header{background: linear-gradient(135deg, #0a2a66 0%, #123d95 100%); color:white; padding:50px 20px; text-align:center}
.header h1{font-size:36px; color:#ffcc00; letter-spacing:1px}.header p{margin:10px 0; opacity:0.9}
.btn{display:inline-block; background:#ffcc00; color:#0a2a66; padding:14px 28px; border-radius:30px; font-weight:800; text-decoration:none; margin:8px; box-shadow:0 4px 12px rgba(0,0,0,0.2)}
.btn-green{background:#25D366; color:white}
.container{max-width:1100px; margin:0 auto; padding:20px}
.services{display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin-top:20px}
.card{background:white; border-radius:16px; padding:20px; box-shadow:0 6px 18px rgba(0,0,0,0.06); border-left:5px solid #0a2a66; transition:0.2s}
.card:hover{transform:translateY(-4px)}.icon{font-size:32px}.card h3{margin:8px 0; color:#0a2a66}
.price{font-weight:800; color:#0a8a28; margin-top:8px}
.order-btn{display:block; margin-top:12px; background:#0a2a66; color:#ffcc00; text-align:center; padding:10px; border-radius:8px; text-decoration:none; font-weight:700}
.trust{background:white; margin:30px 0; padding:20px; border-radius:16px; display:grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap:15px; text-align:center}
.footer{background:#0a2a66; color:white; text-align:center; padding:30px; margin-top:40px}
input, select{width:100%; padding:12px; margin:8px 0; border-radius:8px; border:1px solid #ccc}
</style>
</head>
<body>
<div class="header">
<h1>CYBER MTAANI</h1>
<p>REMOTE CYBER SERVICES • FAST • RELIABLE • 24/7</p>
<p>📞 0706507594 | 📧 remotecyber@gmail.com</p>
<div>
<a class="btn" href="https://wa.me/254706507594?text=Hello%20Cyber%20Mtaani,%20I%20need%20help%20with">💬 WhatsApp Us Now</a>
<a class="btn btn-green" href="tel:0706507594">📞 Call Now</a>
</div>
</div>

<div class="container">
<h2 style="text-align:center; color:#0a2a66; margin:20px 0">Our Services - Pay After Service</h2>

<div class="services">
{% for title, icon, desc, price in services %}
<div class="card">
<div class="icon">{{icon}}</div>
<h3>{{title}}</h3>
<p style="font-size:13px; color:#555">{{desc}}</p>
<p class="price">From KES {{price}}</p>
<a class="order-btn" href="https://wa.me/254706507594?text=Hello,%20I%20need%20{{title}}">Order via WhatsApp</a>
</div>
{% endfor %}
</div>

<div class="trust">
<div><h3>⚡ 10 Min Service</h3><p>Most services done in 10-20 mins remotely</p></div>
<div><h3>🔒 100% Secure</h3><p>Your data is safe & confidential</p></div>
<div><h3>💰 Pay After</h3><p>Pay via M-Pesa Till after service done</p></div>
<div><h3>🇰🇪 All Kenya</h3><p>Serving all 47 counties remotely</p></div>
</div>

<div style="background:white; padding:25px; border-radius:16px; text-align:center">
<h2>How It Works</h2>
<p style="margin:15px 0">1️⃣ WhatsApp us → 2️⃣ Send documents → 3️⃣ We process → 4️⃣ You pay via M-Pesa</p>
<p><b>💚 Lipa na M-Pesa Till: 6534283 - CYBER MTAANI</b></p>
<p style="font-size:13px">Pay after service is confirmed</p>
</div>
</div>

<div class="footer">
<h3>CYBER MTAANI</h3>
<p>Remote Cyber Services Across Kenya</p>
<p style="margin-top:10px">© 2025 Cyber Mtaani | 0706507594 | cybermtaani.onrender.com</p>
<p style="font-size:12px; margin-top:10px; opacity:0.7">Passport • KRA • EPRA • eCitizen • NTSA • HELB • Business Registration</p>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE, services=SERVICES)

@app.route('/admin-king')
def admin():
    db = get_db()
    cur = db.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()
    html = "<h2>Orders Admin</h2><table border=1><tr><th>ID</th><th>Name</th><th>Phone</th><th>Service</th><th>Date</th></tr>"
    for o in orders:
        html+=f"<tr><td>{o[0]}</td><td>{o[1]}</td><td>{o[2]}</td><td>{o[3]}</td><td>{o[5]}</td></tr>"
    html+="</table>"
    return html

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
