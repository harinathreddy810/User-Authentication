from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = '1234'  # MySQL password
app.config['MYSQL_DB'] = 'Aurora'  # Database name

mysql = MySQL(app)

# Registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        idnumber = request.form['idnumber']
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Check if the username already exists
        cur.execute("SELECT * FROM User WHERE username = %s", (username,))
        user_exists = cur.fetchone()

        if user_exists:
            flash("Username already taken. Try a different one.")
            return redirect(url_for('register'))

        # Hash the password before saving it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Insert new user into the database
        cur.execute("INSERT INTO User (idnumber, username, password) VALUES (%s, %s, %s)", 
                    (idnumber, username, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash(f"User {username} registered successfully!")
        return redirect(url_for('login'))

    return render_template('register.html')


# Login page route
@app.route('/')
def login():
    return render_template('login.html')

# Login logic route
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM User WHERE username = %s", (username,))
    user = cur.fetchone()

    if not user:
        flash("Username not found! Please try again or register.")
        return redirect(url_for('login'))

    if not check_password_hash(user[3], password):  # user[3] is the password column
        flash("Incorrect password! Please try again.")
        return redirect(url_for('login'))

    return redirect(url_for('home', username=user[2]))  # user[2] is the username column


# Home page route
@app.route('/home/<username>')
def home(username):
    user = {'username': username}  # Creating a user dictionary
    return render_template('home.html', user=user)

# Attendance page route
@app.route('/attendance')
def attendance():
    return '''
        <h2>Attendance</h2>
        <p>Here are your attendance details...</p>
        <a href="/">Back to Home</a>
    '''


# Results page route
@app.route('/results')
def results():
    return '''
        <h2>Results</h2>
        <p>Here are your exam results...</p>
        <a href="/">Back to Home</a>
    '''


# Academic information page route
@app.route('/academic')
def academic():
    return '''
        <h2>Academic Information</h2>
        <p>Here is your academic information...</p>
        <a href="/">Back to Home</a>
    '''


# Documents page route
@app.route('/documents')
def documents():
    return '''
        <h2>Documents</h2>
        <p>Here are your important documents...</p>
        <a href="/">Back to Home</a>
    '''


# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)
