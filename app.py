import mysql.connector
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps

app = Flask(__name__)

config = {
    'host': 'kelompok2databases.mysql.database.azure.com',
    'user': 'daffa',
    'password': 'Nusantara45_',
    'database': 'db_login',  # Replace with your actual database name
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'
}

# Establish a MySQL connection
mysql_conn = mysql.connector.connect(**config)

# Login
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pass"]
        cur = mysql_conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM login WHERE EMAIL=%s AND PASS=%s", (email, pwd))
        data = cur.fetchone()
        cur.close()
        if data:
            session['logged_in'] = True
            session['username'] = data["NAMA"]
            flash('Login Successfully', 'success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again', 'danger')
    return render_template("login.html")

# check if the user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Registration
@app.route('/reg', methods=['POST', 'GET'])
def reg():
    status = False
    if request.method == 'POST':
        nama = request.form["nama"]
        email = request.form["email"]
        pwd = request.form["pass"]
        cur = mysql_conn.cursor()
        cur.execute("INSERT INTO login(NAMA, EMAIL, PASS) VALUES (%s, %s, %s)", (nama, email, pwd))
        mysql_conn.commit()
        cur.close()
        flash('Registration Successfully. Login Here...', 'success')
        return redirect('login')
    return render_template("reg.html", status=status)

# Home page
@app.route("/home")
@is_logged_in
def home():
    return render_template('home.html')

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
