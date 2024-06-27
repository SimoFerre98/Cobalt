from flask import Flask, render_template, request, redirect, url_for
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# DB Configuration
app.config['MYSQL_HOST'] = '31.11.39.152'
app.config['MYSQL_USER'] = 'Sql1793908'
app.config['MYSQL_PASSWORD'] = 'Lu.Stam100'
app.config['MYSQL_DB'] = 'Sql1793908'

# DB connection
def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Registration page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password_hash) VALUES (%s, %s, %s, %s)',
            (first_name, last_name, email, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Access to the dashboard
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]  # Save the user ID in the session
            return redirect(url_for('dashboard'))
        else:
            error = 'Wrong email or password!'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'member_id' in session:
        # The user is authenticated, show the dashboard
        return render_template('dashboard.html')
    else:
        # The user is not authenticated, redirect to the login page
        return redirect(url_for('login'))

# Logout page
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user ID from the session
    return redirect(url_for('login'))

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects')
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
