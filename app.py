from flask import Flask, render_template_string, request, g, redirect
import sqlite3, os, random, datetime

app = Flask(__name__)
DATABASE = '/tmp/cyber.db'
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
]

PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Mtaani - Kenya Digital Solutions - Till 6534283</title>
<style>
body{font-family:Arial,sans-serif;background:#f5f7fb;margin:0;color:#333}
.h{background:#0a2a66;color:#fff;padding:50px 20px;text-align:center}
.h h1{color:#ffcc00;font-size:42px;margin:0;letter-spacing:2px}
.h p{color:#fff;margin:10px 0}
.b{background:#ffcc00;color:#0a2a66;padding:14px 28px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:8px;font-size:16px}
.b2{background:#25D366;color:#fff;padding:14px 28px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:8px}
.c{max-width:1100px;margin:auto;padding:20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px}
.card{background:#fff;padding:20px;border-radius:14px;border-left:5px solid #0a2a66;box-shadow:0 4px 10px rgba(0,0,0,0.08);transition:0.2s}
.card:hover{transform:translateY(-4px)}
.card h3{margin:8px 0;color:#0a2a66}
.card p{font-size:13px;color:#666;margin:5px 0}
.btn{display:block;background:#0a2a66;color:#ffcc00;text-align:center;padding:10px;border-radius:8px;text-decoration:none;font-weight:800;margin-top:10px}
.trust{background:#fff;padding:20px;border-radius:12px;margin-top:25px;text-align:center;border:2px solid #0a2a66}
.f{background:#0a2a66;color:#fff;text-align:center;padding:25px;margin-top:30px;line-height:1.6}
</style></head><body>
<div class="h">
<h1>CYBER MTAANI</h1>
<p style="font-size:18px;font-weight:700">Kenya Digital Solutions | All 47 Counties | Fast • 10 Minutes</p>
<p>Trusted • Professional • Reliable • Nationwide</p>
<div style="margin-top:20px">
<a class="b" href="https://wa.me/254706507594">💬 WhatsApp Us</a>
<a class="b2" href="https://wa.me/254706507594?text=Habari%20Cyber%20Mtaani%2C%20nahitaji%20huduma">📲 Order Now</a>
</div>
</div>

<div class="c">
<h2 style="text-align:center;color:#0a2a66;font-size:26px">OUR SERVICES - All Government Services Available</h2>
<p style="text-align:center;color:#666">Click any service to order via WhatsApp - Pay via Till</p>
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

<div class="trust">
<h3 style="color:#0a2a66;margin-top:0">💚 Lipa na M-Pesa - Till Number: {{till}} - CYBER MTAANI</h3>
<p><b>How it works:</b> 1. WhatsApp Us 2. Send Details 3. We Process in 10 Min 4. Pay to Till {{till}} 5. Get Receipt + Document</p>
<p style="background:#e8f5e9;padding:10px;border-radius:8px;color:#2e7d32;font-weight:800">✅ Pay After Service • Professional Receipt Issued • Available 24/7</p>
</div>

<div style="background:#0a2a66;color:#fff;padding:20px;border-radius:12px;margin-top:20px;text-align:center">
<h3 style="color:#ffcc00;margin:0">📞 Need Help? Talk to Us Now</h3>
<p>Website: cybermtaani.onrender.com | WhatsApp: 0706507594 | Till: {{till}}</p>
</div>

</div>
<div class="f">
<b style="color:#ffcc00;font-size:18px">CYBER MTAANI - Kenya Digital Solutions</b><br>
🌐 cybermtaani.onrender.com | 💬 0706507594 | 💚 Till {{till}}<br>
Professional • Reliable • Trusted Across Kenya • All 47 Counties<br>
© 2025 Cyber Mtaani - Licensed Digital Services Provider
</div>
</body></html>
"""

@app.route('/')
def home(): return render_template_string(PAGE, services=SERVICES, till=TILL)

@app.route('/admin-king')
def admin():
    db=get_db(); orders=db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    h=f"<div style='font-family:Arial;padding:20px'><h2>Admin - Cyber Mtaani Till {TILL}</h2><form method=post action=/add-order style='background:#eee;padding:15px;border-radius:10px'><input name=name placeholder='Customer Name' required> <input name=phone placeholder='Phone' required> <input name=service placeholder='Service' required> <input name=amount placeholder='Amount Charged' required> <button style='background:#0a2a66;color:#ffcc00;padding:8px 15px;border:none;border-radius:5px;font-weight:800'>Generate Receipt</button></form><hr><table border=1 cellpadding=8 style='width:100%;border-collapse:collapse'><tr style='background:#0a2a66;color:#ffcc00'><th>ID</th><th>Receipt</th><th>Name</th><th>Service</th><th>Amount</th><th>View</th></tr>"
    for o in orders: h+=f"<tr><td>{o[0]}</td><td>CM-{o[5]}</td><td>{o[1]}</td><td>{o[3]}</td><td>{o[4]}</td><td><a href=/receipt/{o[0]}>View Receipt</a></td></tr>"
    return h+"</table></div>"

@app.route('/receipt/<int:oid>')
def receipt(oid):
    db=get_db(); o=db.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
    if not o: return "Not found"
    return f"""<div style='max-width:400px;margin:30px auto;background:#fff;padding:25px;border-radius:12px;box-shadow:0 0 20px rgba(0,0,0,0.15);font-family:Arial;border-top:6px solid #0a2a66'><h2 style='text-align:center;color:#0a2a66;margin:0'>CYBER MTAANI</h2><p style='text-align:center;font-size:12px;color:#666;margin:5px'>Kenya Digital Solutions<br>Till {TILL} | 0706507594<br>cybermtaani.onrender.com</p><hr><p><b>Receipt No:</b> CM-{o[5]}<br><b>Date:</b> {o[6]}<br><b>Customer:</b> {o[1]}<br><b>Phone:</b> {o[2]}<br><b>Service:</b> {o[3]}<br><b>Amount Paid:</b> KES {o[4]}<br><b>Status:</b> <span style='color:green;font-weight:800'>PAID & VERIFIED</span></p><hr><div style='border:3px solid #2e7d32;color:#2e7d32;text-align:center;padding:10px;border-radius:8px;font-weight:900;font-size:18px'>✓ PAID VIA TILL {TILL}</div><p style='font-size:11px;text-align:center;color:#666;margin-top:15px'>Thank you for choosing Cyber Mtaani!<br>Professional • Reliable • Trusted<br>Receipt is valid proof of payment</p></div>"""

@app.route('/add-order',methods=['POST'])
def add():
    r=str(random.randint(10000,99999)); d=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    db=get_db(); db.execute("INSERT INTO orders (name,phone,service,amount,receipt_no,date,status) VALUES (?,?,?,?,?,?,?)",(request.form['name'],request.form['phone'],request.form['service'],request.form['amount'],r,d,'Paid')); db.commit()
    oid=db.execute("SELECT last_insert_rowid()").fetchone()[0]; return redirect(f"/receipt/{oid}")

@app.teardown_appcontext
def close(e):
    db=getattr(g,'_database',None);
    if db: db.close()
