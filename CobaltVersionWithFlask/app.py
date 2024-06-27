from flask import Flask,render_template,url_for
import MySQLdb

# template_folder is the folder where the HTML files are stored.
# static_folder is the folder where the CSS, JS and image files are stored.
app = Flask(__name__, template_folder='public/html',static_folder='public')

# Configurazione del database
app.config['MYSQL_HOST'] = '31.11.39.152'
app.config['MYSQL_USER'] = 'Sql1793908'
app.config['MYSQL_PASSWORD'] = 'Lu.Stam100'
app.config['MYSQL_DB'] = 'Sql1793908'
app.config['MYSQL_PORT'] = 3306

# Funzione per ottenere la connessione al database
def get_db_connection():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config.get('MYSQL_PORT'),
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Default route 
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM members')
    data = cursor.fetchall()
    connection.close()
    # Stampa i dati nel terminale
    print("Dati recuperati dal database:")
    for row in data:
        print(row)    
    return render_template('index.html',data = data)

# Login route
@app.route('/login')
def login():
    return render_template('login.html')

# Signup route
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True) # Run the app in debug mode. This will automatically restart the server for you after you make changes to the code.