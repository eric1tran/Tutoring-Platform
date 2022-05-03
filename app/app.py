from dotenv import load_dotenv
from flask import Flask, render_template
import os, sys

app = Flask(__name__)

load_dotenv()

if not os.getenv("DATABASE_URL"):
    print(f"DATABASE_URL is not set. Create a .env file and set it if it doesn't exist")
    sys.exit(1)

@app.route('/')
def index():
    # GET - Display login page

    # POST - Validate login information and login and forward to user home page

    return render_template('login.html')

@app.route('/signup')
def signup():
    # GET - Returns HTML forms to get user information

    # POST - Calls backend servers to validate user information and create an account

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)