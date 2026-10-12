from flask import Flask, render_template_string, request, g, redirect, send_from_directory
import sqlite3, os, random, datetime

app = Flask(__name__)
DATABASE = 'cyber.db'
TILL = "6534283"

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
        receipt_no TEXT, status TEXT, date TEXT)""")
    db.commit(); db.close()

init_db()

SERVICES = [
    ("Passport Application","🛂","New / Renewal / Lost - All Types"),
    ("EPRA License","⚡","T1 T2 T3 C1 - Avoid 5K EPRA Fine"),
    ("KRA PIN & Returns","🧾","New PIN, Nil, PAYE, Turnover - 10 Min"),
    ("Good Conduct","🏛️","DCI Certificate - Fast Processing"),
    ("Business Registration","🏢","Business Name, Company, Permits"),
    ("CV & Cover Letter","📄","Professional CV - ATS Compliant"),
    ("HELB / NTSA / SHA","🎓","Compliance, Loans, Driving License"),
    ("eCitizen Services","💻","All Govt Services - 47 Counties"),

    {
  "id": "website-design",
  "name": "Website Design",
  "icon": "🎨",
  "price": 5000,
  "description": "Professional modern website design - business, portfolio, landing page. Mobile-friendly, fast, with M-Pesa integration.",
  "delivery": "3 Days"
},
{
  "id": "website-development",
  "name": "Website Development",
  "icon": "💻",
  "price": 15000,
  "description": "Full website development - eCommerce, booking system, cyber portal like Cyber Mtaani. Hosting + domain + M-Pesa Till + admin panel included.",
  "delivery": "7 Days"
},
]

PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Mtaani - Kenya Digital Solutions - Till 6534283</title>
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/favicon.png">
<style>
body{font-family:Arial,sans-serif;background:#f5f7fb;margin:0;color:#333}
.h{background:#0a2a66;color:#fff;padding:50px 20px;text-align:center}
.h h1{color:#ffcc00;font-size:42px;margin:0;letter-spacing:2px}
.h p{color:#fff;margin:10px 0}
.b{background:#ffcc00;color:#0a2a66;padding:14px 28px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:8px;font-size:16px}
.b2{background:#25D366;color:#fff;padding:14px 28px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:8px}
.c{max-width:1100px;margin:auto;padding:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px}
.card{background:#fff;padding:20px;border-radius:14px;border-left:5px solid #0a2a66;box-shadow:0 4px 10px rgba(0,0,0,0.08)}
.card h3{margin:8px 0;color:#0a2a66}
.card p{font-size:13px;color:#666;margin:5px 0}
.btn{display:block;background:#0a2a66;color:#ffcc00;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:800;margin-top:10px}
.f{background:#0a2a66;color:#fff;text-align:center;padding:30px;margin-top:30px;line-height:1.8}
.f b{color:#ffcc00}
</style></head><body>
<div class="h">
<h1>CYBER MTAANI</h1>
<p style="font-size:13px;letter-spacing:3px;color:#25D366;font-weight:800">Kenya Digital Solutions</p>
<p style="font-size:16px;font-weight:700">All 47 Counties | Fast • 10 Minutes • Trusted Nationwide</p>
<div style="margin-top:20px">
<a class="b" href="https://wa.me/254706507594">💬 WhatsApp Us</a>
<a class="b2" href="https://wa.me/254706507594?text=Habari%20Cyber%20Mtaani%2C%20nahitaji%20huduma">📲 Order Now</a>
</div>
</div>

<div class="c">
<h2 style="text-align:center;color:#0a2a66;font-size:26px">OUR SERVICES - All Government Services Available</h2>
<p style="text-align:center;color:#666">Click any service to order via WhatsApp</p>
<div class="grid">
{% for t,i,d in services %}
<div class="card">
<div style="font-size:36px">{{i}}</div>
<h3>{{t}}</h3>
<p>{{d}}</p>
<a class="btn" href="https://wa.me/254706507594?text=Habari%2C%20nahitaji%20{{t}}">Chat for Price →</a>
</div>
{% endfor %}
</div>
</div>

<div class="f">
<b style="font-size:20px">CYBER MTAANI - Kenya Digital Solutions</b><br>
💚 Lipa na M-Pesa Till: {{till}} | Professional Receipt Issued | Pay After Service<br>
🌐 cybermtaani.onrender.com | 💬 WhatsApp: 0706507594 | Available 24/7<br>
Trusted Across Kenya • All 47 Counties • Secure • Reliable<br>
© 2026 Cyber Mtaani
</div>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(PAGE, services=SERVICES, till=TILL)

@app.route('/favicon.png')
def favicon():
    try:
        return send_from_directory('.', 'favicon.png')
    except:
        return "", 404

@app.route('/logo.png')
def logo():
    try:
        return send_from_directory('.', 'logo.png')
    except:
        return "", 404

@app.route('/admin-king')
def admin():
    db=get_db(); orders=db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    h=f"<div style='font-family:Arial;padding:20px'><h2>Admin - Till {TILL}</h2><form method=post action=/add-order style='background:#eee;padding:15px;border-radius:10px'><input name=name placeholder='Customer Name' required> <input name=phone placeholder='Phone' required> <input name=service placeholder='Service' required> <input name=amount placeholder='Amount' required> <button style='background:#0a2a66;color:#ffcc00;padding:8px 15px;border:none;border-radius:5px;font-weight:800'>Generate Receipt</button></form><hr><table border=1 cellpadding=8 style='width:100%;border-collapse:collapse'><tr style='background:#0a2a66;color:#ffcc00'><th>ID</th><th>Receipt</th><th>Name</th><th>Service</th><th>Amount</th><th>View</th></tr>"
    for o in orders: h+=f"<tr><td>{o[0]}</td><td>CM-{o[5]}</td><td>{o[1]}</td><td>{o[3]}</td><td>{o[4]}</td><td><a href=/receipt/{o[0]}>Receipt</a></td></tr>"
    return h+"</table></div>"

@app.route('/receipt/<int:oid>')
def receipt(oid):
    db=get_db(); o=db.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
    if not o: return "Not found"
    return f"""<div style='max-width:400px;margin:30px auto;background:#fff;padding:25px;border-radius:12px;box-shadow:0 0 20px rgba(0,0,0,0.15);font-family:Arial;border-top:6px solid #0a2a66'><div style='text-align:center'><img src='/favicon.png' style='width:60px' onerror=\"this.style.display='none'\"></div><h2 style='text-align:center;color:#0a2a66;margin:10px 0 0'>CYBER MTAANI</h2><p style='text-align:center;font-size:12px;color:#666;margin:5px'>Kenya Digital Solutions<br>Till {TILL} | 0706507594<br>cybermtaani.onrender.com</p><hr><p><b>Receipt No:</b> CM-{o[5]}<br><b>Date:</b> {o[6]}<br><b>Customer:</b> {o[1]}<br><b>Phone:</b> {o[2]}<br><b>Service:</b> {o[3]}<br><b>Amount Paid:</b> KES {o[4]}<br><b>Status:</b> <span style='color:green;font-weight:800'>PAID & VERIFIED</span></p><hr><div style='border:3px solid #2e7d32;color:#2e7d32;text-align:center;padding:10px;border-radius:8px;font-weight:900;font-size:18px'>✓ PAID VIA TILL {TILL}</div><p style='font-size:11px;text-align:center;color:#666;margin-top:15px'>Thank you for choosing Cyber Mtaani!</p></div>"""

@app.route('/add-order',methods=['POST'])
def add():
    r=str(random.randint(10000,99999)); d=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    db=get_db(); db.execute("INSERT INTO orders (name,phone,service,amount,receipt_no,date,status) VALUES (?,?,?,?,?,?,?)",(request.form['name'],request.form['phone'],request.form['service'],request.form['amount'],r,d,'Paid')); db.commit()
    oid=db.execute("SELECT last_insert_rowid()").fetchone()[0]; return redirect(f"/receipt/{oid}")

@app.teardown_appcontext
def close(e):
    db=getattr(g,'_database',None);
    if db: db.close()
