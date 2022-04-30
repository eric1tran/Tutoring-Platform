from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys

app = Flask(__name__)

load_dotenv()

if not os.getenv("DATABASE_URL"):
    print(f"DATABASE_URL is not set. Create a .env file and set it if it doesn't exist")
    sys.exit(1)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return '<h1>Tutoring Platform</h1>'

if __name__ == '__main__':
    app.run(debug=True)