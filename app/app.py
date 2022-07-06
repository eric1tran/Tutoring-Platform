from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for
import os, sys


from database import MySqlDBConnection, hash_password

app = Flask(__name__)

app.secret_key = "12345"

load_dotenv()

if not os.getenv("DATABASE_URL"):
    print(f"DATABASE_URL is not set. Create a .env file and set it if it doesn't exist")
    sys.exit(1)


# Log In endpoint
@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session and session['loggedin']:
        print('logged in')
        return render_template('home.html', name=session['name'])

    error = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "" or password == "":
            error = "Missing input field(s)"
            return render_template("login.html", error=error)

        # Validate credentials
        with MySqlDBConnection(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), "tutoring_db") as db:
            cursor = db.session.cursor(dictionary=True)

            query = ("SELECT id, first, last, email, password FROM users where email = %s")
            cursor.execute(query, (email,))
            data = cursor.fetchall()
            if not data:
                print(f'Account {email} does not exist.')
                error = "Account/password combination do not exist"
            else:
                db_result = data[0]
                user_id = db_result['id']
                password_db = db_result['password']
                password_input = hash_password(password)

                if password_db != password_input:
                    error = "Invalid Password!"
                else:
                    # Session cookies
                    session['loggedin'] = True
                    session['id'] = user_id
                    session['name'] = f'{db_result["first"]} {db_result["last"]}'
                    return render_template('home.html', name=session['name'])
                    #return redirect(url_for('home'))

    return render_template('login.html', error=error)

# Sign Up endpoint
@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    error = None

    if request.method == 'POST':
        first = request.form['firstname']
        last = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        if email == "" or password == "" or first == "" or last == "":
            error = "Missing input field(s)"
            return render_template("signup.html", error=error)

        # TODO: server side email address validation

        with MySqlDBConnection(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), "tutoring_db") as db:
            cursor = db.session.cursor()

            # Check if account exists already
            query = ("SELECT * FROM users where email = %s")
            cursor.execute(query, (email,))
            data = cursor.fetchall()
            if data:
                print(f'An account with that email already exists')
                error = f'An account with that email already exists'
            else:
                password_hash = hash_password(password)
                if not password_hash:
                    error = f'Invalid password format'
                    return render_template('signup.html', error=error)

                print(f'Creating account for {first} {last} with email {email}')
                query = ("INSERT INTO users (first, last, email, user_type, password) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(query, (first, last, email, 'admin', password_hash))
                db.session.commit()

                return render_template('home.html', name=f'{first} {last}')

    return render_template('signup.html', error=error)

@app.route('/home', methods=['GET','POST'])
def home():
    if 'loggedin' in session and session['loggedin']:
        return render_template('home.html', name=session['name'])

    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return "My Profile"

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)