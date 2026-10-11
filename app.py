from flask import Flask, render_template_string, request, g
import sqlite3, datetime, os, random

app = Flask(__name__)
DATABASE = 'cyber.db'
TILL = "6534283"
BUSINESS = "CYBER MTAANI"

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
        receipt_no TEXT, status TEXT DEFAULT 'Pending', date TEXT
    )""")
    db.commit(); db.close()

SERVICES = [
    ("Passport Application", "🛂", "New, Renewal, Lost", "500"),
    ("EPRA License T1 T2 T3 C1", "⚡", "Electrician & Solar License", "800"),
    ("KRA PIN Registration", "🧾", "In 10 Minutes", "300"),
    ("KRA Tax Returns", "💰", "Nil, PAYE, Turnover", "500"),
    ("Good Conduct DCI", "🏛️", "Police Clearance", "600"),
    ("Business Registration", "🏢", "Company, Business Name", "1500"),
    ("CV & Cover Letter", "📄", "Professional ATS CV", "400"),
    ("HELB / NTSA / SHA", "🎓", "Compliance", "600"),
]

HOME = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cyber Mtaani - Remote Cyber Kenya</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Segoe UI,Arial;background:#f5f7fb}
.header{background:linear-gradient(135deg,#0a2a66,#123d95);color:#fff;padding:45px 20px;text-align:center}
.header h1{color:#ffcc00;font-size:34px}.btn{display:inline-block;background:#ffcc00;color:#0a2a66;padding:12px 22px;border-radius:30px;font-weight:800;text-decoration:none;margin:6px}
.btn-green{background:#25D366;color:#fff}.container{max-width:1100px;margin:0 auto;padding:20px}
.services{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.card{background:#fff;border-radius:14px;padding:18px;box-shadow:0 5px 15px rgba(0,0,0,.06);border-left:5px solid #0a2a66}
.price{font-weight:800;color:#0a8a28}.order-btn{display:block;margin-top:10px;background:#0a2a66;color:#ffcc00;text-align:center;padding:9px;border-radius:8px;text-decoration:none;font-weight:700}
.footer{background:#0a2a66;color:#fff;text-align:center;padding:25px;margin-top:30px}
</style></head><body>
<div class="header">
<h1>CYBER MTAANI</h1><p>REMOTE CYBER SERVICES • 24/7 • ALL 47 COUNTIES</p>
<p>📞 0706507594 | 💚 Till: 6534283</p>
<div><a class="btn" href="https://wa.me/254706507594">💬 WhatsApp Order</a>
<a class="btn btn-green" href="#services">Services</a></div></div>
<div class="container" id="services">
<h2 style="text-align:center;color:#0a2a66;margin:15px">Our Services</h2>
<div class="services">
{% for title, icon, desc, price in services %}
<div class="card"><div style="font-size:28px">{{icon}}</div><h3>{{title}}</h3><p style="font-size:13px;color:#555">{{desc}}</p>
<p class="price">KES {{price}}</p><a class="order-btn" href="https://wa.me/254706507594?text=Habari%20Cyber%20Mtaani,%20nahitaji%20{{title}}%20-%20Niko%20tayari%20kulipa%20Till%20{{till}}">Order Now</a></div>
{% endfor %}</div>
<div style="background:#fff;padding:20px;border-radius:14px;margin-top:25px;text-align:center">
<h3>How to Pay & Get Receipt</h3><p>1. WhatsApp us → 2. We do service → 3. Pay to Till <b>{{till}}</b> → 4. Get Auto Receipt + Document on WhatsApp</p>
<p style="margin-top:10px;background:#e8f5e9;padding:10px;border-radius:8px">💚 <b>Lipa na M-Pesa</b> → Buy Goods → Till: <b>{{till}}</b> - CYBER MTAANI<br>After payment, send M-Pesa message for instant receipt</p>
</div></div>
<div class="footer"><h3>CYBER MTAANI</h3><p>© 2025 | Till: {{till}} | cybermtaani.onrender.com | 0706507594</p></div>
</body></html>
"""

RECEIPT_HTML = """
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>
body{font-family:Arial; background:#f0f0f0; padding:20px}.paper{background:#fff; max-width:400px; margin:0 auto; padding:25px; border-radius:10px; border-top:6px solid #0a2a66}
h2{text-align:center; color:#0a2a66}.row{display:flex; justify-content:space-between; margin:8px 0; font-size:14px}
hr{border:none; border-top:1px dashed #ccc; margin:15px 0}.stamp{text-align:center; margin-top:20px; border:2px solid #0a8a28; color:#0a8a28; padding:8px; border-radius:8px; font-weight:800; transform:rotate(-3deg)}
.btn{display:block; text-align:center; background:#25D366; color:#fff; padding:12px; border-radius:8px; text-decoration:none; margin-top:15px; font-weight:700}
</style></head><body>
<div class="paper">
<h2>CYBER MTAANI</h2><p style="text-align:center; font-size:12px">Remote Cyber Services | 0706507594<br>Till: {{till}}</p><hr>
<div class="row"><b>Receipt No:</b><span>CM-{{receipt}}</span></div>
<div class="row"><b>Date:</b><span>{{date}}</span></div>
<div class="row"><b>Customer:</b><span>{{name}}</span></div>
<div class="row"><b>Phone:</b><span>{{phone}}</span></div>
<div class="row"><b>Service:</b><span>{{service}}</span></div>
<div class="row"><b>Amount:</b><span>KES {{amount}}</span></div>
<div class="row"><b>Payment:</b><span>M-Pesa Till {{till}}</span></div>
<div class="row"><b>Status:</b><span style="color:green">✅ PAID & COMPLETED</span></div>
<hr><p style="font-size:11px; text-align:center">Thank you for choosing Cyber Mtaani! Your document has been sent via WhatsApp.</p>
<div class="stamp">PAID ✔ VERIFIED</div>
<a class="btn" href="https://wa.me/254706507594?text=Receipt%20{{receipt}}%20confirmed">Share Receipt on WhatsApp</a>
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HOME, services=SERVICES, till=TILL)

@app.route('/receipt/<int:order_id>')
def receipt(order_id):
    db = get_db()
    cur = db.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    o = cur.fetchone()
    if not o: return "Receipt not found"
    return render_template_string(RECEIPT_HTML, receipt=o[5], date=o[6], name=o[1], phone=o[2], service=o[3], amount=o[4], till=TILL)

@app.route('/admin-king')
def admin():
    db = get_db()
    cur = db.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cur.fetchall()
    html = f"""
    <h2>Cyber Mtaani Admin - Till {TILL}</h2>
    <form method='post' action='/add-order' style='background:#f5f5f5;padding:15px;border-radius:8px'>
    <h3>Add New Paid Order + Generate Receipt</h3>
    <input name='name' placeholder='Customer Name' required>
    <input name='phone' placeholder='Phone e.g. 0706...' required>
    <select name='service'><option>Passport Application</option><option>EPRA License</option><option>KRA PIN</option><option>KRA Returns</option><option>Good Conduct</option><option>Business Registration</option><option>CV</option><option>HELB/NTSA/SHA</option></select>
    <input name='amount' placeholder='Amount e.g. 500' required>
    <button type='submit'>Generate Receipt</button></form><hr>
    <table border=1 cellpadding=6><tr><th>ID</th><th>Receipt</th><th>Name</th><th>Service</th><th>Amount</th><th>Link</th></tr>
    """
    for o in orders:
        html+=f"<tr><td>{o[0]}</td><td>{o[5]}</td><td>{o[1]}</td><td>{o[3]}</td><td>{o[4]}</td><td><a href='/receipt/{o[0]}' target='_blank'>View Receipt</a> | <a href='https://wa.me/{o[2]}?text=Here is your receipt: https://cybermtaani.onrender.com/receipt/{o[0]}' target='_blank'>Send WhatsApp</a></td></tr>"
    html+="</table>"
    return html

@app.route('/add-order', methods=['POST'])
def add_order():
    name = request.form['name']; phone = request.form['phone']; service = request.form['service']; amount = request.form['amount']
    receipt_no = str(random.randint(10000,99999))
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    db = get_db()
    db.execute("INSERT INTO orders (name,phone,service,amount,receipt_no,date,status) VALUES (?,?,?,?,?,?,?)", (name,phone,service,amount,receipt_no,date,'Paid'))
    db.commit()
    cur = db.execute("SELECT last_insert_rowid()"); oid = cur.fetchone()[0]
    return redirect(f"/receipt/{oid}")

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

# Initialize database on startup (important for Render)
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT",5000)))
