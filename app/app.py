from dotenv import load_dotenv
from flask import Flask, render_template, request
import mysql.connector
import os, sys

from database import MySqlDBConnection

app = Flask(__name__)

load_dotenv()

if not os.getenv("DATABASE_URL"):
    print(f"DATABASE_URL is not set. Create a .env file and set it if it doesn't exist")
    sys.exit(1)


@app.route('/', methods=['GET','POST'])
def index():
    # GET - Display user home page if logged in, otherwise the login page

    # POST - Validate login information and login and forward to user home page
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # GET - Returns HTML forms to get user information

    # POST - Calls backend servers to validate user information and create an account
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with MySqlDBConnection(os.getenv('DB_HOST'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), "tutoring_db") as db:
            cursor = db.session.cursor()
            query = ("SELECT * FROM users")

            cursor.execute(query)

            for result in cursor:
                print(result)

        # Check if email exists
        # If yes, return response saying There is an account under this email. Log in
        # If no, add an entry into users table and then respond saying account created

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)