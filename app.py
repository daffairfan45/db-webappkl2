import pyodbc
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps

app = Flask(__name__)

# Konfigurasi Azure SQL Server
server = 'mysqllogin.database.windows.net'
database = 'dbdbkelompok2'
username = 'daffa'
password = 'Nusantara45_'
driver = '{ODBC Driver 17 for SQL Server}'

# Membangun koneksi ke Azure SQL Server
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
sql_conn = pyodbc.connect(conn_str)

# Fungsi decorator untuk memeriksa apakah pengguna sudah login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Mohon login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
    return wrap

# Halaman login
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    status = True
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["pass"]
        cursor = sql_conn.cursor()
        cursor.execute("SELECT * FROM dblogin WHERE EMAIL=? AND PASS=?", (email, pwd))
        data = cursor.fetchone()
        cursor.close()
        if data:
            session['logged_in'] = True
            session['username'] = data.NAMA
            flash('Login Berhasil', 'success')
            return redirect('home')
        else:
            flash('Login Gagal. Coba lagi', 'danger')
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
        cur = sql_conn.cursor()  # Ganti mysql_conn menjadi sql_conn
        cur.execute("INSERT INTO dblogin(NAMA, EMAIL, PASS) VALUES (?, ?, ?)", (nama, email, pwd))  # Menggunakan tanda tanya (?) untuk parameter
        sql_conn.commit()
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
