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
    ("Passport Application","🛂","New/Renewal/Lost","500"),
    ("EPRA License","⚡","T1 T2 T3 C1 - Avoid 5K fine","800"),
    ("KRA PIN","🧾","In 10 Minutes","300"),
    ("KRA Returns","💰","Nil/PAYE/Turnover","500"),
    ("Good Conduct","🏛️","DCI Clearance","600"),
    ("Business Registration","🏢","Company Name","1500"),
    ("CV & Cover Letter","📄","Pro CV","400"),
    ("HELB/NTSA/SHA","🎓","Compliance","600"),
]

PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Mtaani - Till 6534283</title>
<style>body{font-family:Arial;background:#f5f7fb;margin:0}.h{background:#0a2a66;color:#fff;padding:40px;text-align:center}
.h h1{color:#ffcc00}.b{background:#ffcc00;color:#0a2a66;padding:12px 20px;border-radius:25px;text-decoration:none;font-weight:800;display:inline-block;margin:5px}
.c{max-width:1100px;margin:auto;padding:15px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.card{background:#fff;padding:16px;border-radius:12px;border-left:4px solid #0a2a66}.p{color:green;font-weight:800}
.f{background:#0a2a66;color:#fff;text-align:center;padding:20px;margin-top:20px}</style></head><body>
<div class="h"><h1>CYBER MTAANI</h1><p>Remote Cyber Services Kenya | Till 6534283 | 0706507594</p>
<a class="b" href="https://wa.me/254706507594">WhatsApp Us</a> <a class="b" style="background:#25D366;color:#fff" href="https://wa.me/254706507594?text=Habari%20Cyber%20Mtaani">Order Now</a></div>
<div class="c"><h2 style="text-align:center;color:#0a2a66">Services - Pay via Till {{till}}</h2><div class="grid">
{% for t,i,d,p in services %}<div class="card"><div style="font-size:28px">{{i}}</div><h3>{{t}}</h3><p style="font-size:12px;color:#666">{{d}}</p><p class="p">KES {{p}}</p>
<a href="https://wa.me/254706507594?text=Nahitaji%20{{t}}" style="display:block;background:#0a2a66;color:#ffcc00;text-align:center;padding:8px;border-radius:6px;text-decoration:none">Order</a></div>{% endfor %}
</div><div style="background:#fff;padding:15px;border-radius:10px;margin-top:20px;text-align:center"><b>💚 Lipa na M-Pesa Till: {{till}} - CYBER MTAANI</b><br>Pay after service | Receipt issued</div></div>
<div class="f">© 2025 Cyber Mtaani | cybermtaani.onrender.com | 0706507594 | Till {{till}}</div></body></html>
"""

@app.route('/')
def home(): return render_template_string(PAGE, services=SERVICES, till=TILL)

@app.route('/admin-king')
def admin():
    db=get_db(); orders=db.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    h=f"<h2>Admin - Till {TILL}</h2><form method=post action=/add-order style='background:#eee;padding:10px'><input name=name placeholder=Name required><input name=phone placeholder=Phone required><input name=service placeholder=Service required><input name=amount placeholder=Amount required><button>Generate Receipt</button></form><hr><table border=1><tr><th>ID</th><th>Receipt</th><th>Name</th><th>Service</th><th>Amount</th><th>View</th></tr>"
    for o in orders: h+=f"<tr><td>{o[0]}</td><td>{o[5]}</td><td>{o[1]}</td><td>{o[3]}</td><td>{o[4]}</td><td><a href=/receipt/{o[0]}>Receipt</a></td></tr>"
    return h+"</table>"

@app.route('/receipt/<int:oid>')
def receipt(oid):
    db=get_db(); o=db.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
    if not o: return "Not found"
    return f"<div style='max-width:380px;margin:auto;background:#fff;padding:20px;border-top:5px solid #0a2a66'><h2 style='text-align:center;color:#0a2a66'>CYBER MTAANI</h2><p style='text-align:center;font-size:12px'>Till {TILL} | 0706507594</p><hr><p>Receipt: CM-{o[5]}<br>Date: {o[6]}<br>Customer: {o[1]}<br>Phone: {o[2]}<br>Service: {o[3]}<br>Amount: KES {o[4]}<br>Status: PAID</p><hr><div style='border:2px solid green;color:green;text-align:center;padding:6px'>PAID VERIFIED</div><p style='font-size:11px;text-align:center'>Thank you!</p></div>"

@app.route('/add-order',methods=['POST'])
def add():
    r=str(random.randint(10000,99999)); d=datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    db=get_db(); db.execute("INSERT INTO orders (name,phone,service,amount,receipt_no,date,status) VALUES (?,?,?,?,?,?,?)",(request.form['name'],request.form['phone'],request.form['service'],request.form['amount'],r,d,'Paid')); db.commit()
    oid=db.execute("SELECT last_insert_rowid()").fetchone()[0]; return redirect(f"/receipt/{oid}")

@app.teardown_appcontext
def close(e):
    db=getattr(g,'_database',None);
    if db: db.close()
