import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from app.information import info

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", name = info['name'], location = info['location'], url=os.getenv("URL"))

@app.route("/hobbies")
def hobbies():
    return render_template('hobbies.html', url=os.getenv("URL"))
