from dotenv import load_dotenv
from flask import Flask, render_template, request
import mysql.connector
import os, sys

from database import MySqlDBConnection, hash_password

app = Flask(__name__)

load_dotenv()

if not os.getenv("DATABASE_URL"):
    print(f"DATABASE_URL is not set. Create a .env file and set it if it doesn't exist")
    sys.exit(1)


# Login page
@app.route('/', methods=['GET','POST'])
def index():
    # GET - Display user home page if logged in, otherwise the login page

    error = None
    # POST - Validate login information and login and forward to user home page
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == "" or password == "":
            print(f'Missing input')
            return render_template("signup.html")

        # Check if account exists
        with MySqlDBConnection(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), "tutoring_db") as db:
            cursor = db.session.cursor(dictionary=True)

            query = ("SELECT first, last, email, password FROM users where email = %s")
            cursor.execute(query, (email,))
            data = cursor.fetchall()
            if not data:
                print(f'Account {email} does not exist.')
                error = "Account does not exist!"
            else:
                db_result = data[0]
                password_db = db_result['password']
                password_input = hash_password(password)

                if password_db != password_input:
                    error = "Invalid Password!"
                else:
                    fullname = f'{db_result["first"]} {db_result["last"]}'
                    return render_template('home.html', name=fullname)

    return render_template('index.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # GET - Returns HTML forms to get user information

    error = None
    # POST - Calls backend servers to validate user information and create an account
    if request.method == 'POST':
        first = request.form['firstname']
        last = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        if email == "" or password == "" or first == "" or last == "":
            print(f'Missing input')
            # RETURN MISSING INPUT RESPONSE
            return render_template("signup.html")

        # Do server side email address validation as well, return invalid email response if bad

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
                    print(f'Invalid password format')

                print(f'Creating account for {first} {last} using email {email}!')
                query = ("INSERT INTO users (first, last, email, user_type, password) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(query, (first, last, email, 'admin', password_hash))
                db.session.commit()

                return render_template('home.html', name=f'{first} {last}')

    return render_template('signup.html', error=error)

@app.route('/home/<name>')
def home(name):
    return render_template('signup.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)