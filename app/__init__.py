import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from app.information import info
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user = os.getenv("MYSQL_USER"),
        password = os.getenv("MYSQL_PASSWORD"),
        host = os.getenv("MYSQL_HOST"),
        port = 3306
    )

print(mydb)
class TimelinePost(Model):
    name=CharField()
    email=CharField()
    content=TextField()
    created_at=DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])
@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", name = info['name'], location = info['location'], url=os.getenv("URL"))

@app.route("/hobbies")
def hobbies():
    return render_template('hobbies.html', url=os.getenv("URL"))

@app.route("/mail.php", methods=["POST"])
def mail():
    return render_template('index.html', title="MLH Fellow", name = info['name'], location = info['location'], url=os.getenv("URL"))

@app.route("/api/timeline_post", methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts' : [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return {'error': 'Invalid name'}, 400
    if not email:
        return {'error': 'Invalid email'}, 400
    if not content:
        return {'error': 'Invalid content'}, 400

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    if match is None:
        return {'error': 'Invalid email'}, 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

# @app.route('/api/timeline_post/<id>', methods=['DELETE'])
# def delete_time_line_post(id):
#     timeline_post = TimelinePost.delete_by_id(id)
#     return model_to_dict(timeline_post)

@app.route("/api/timeline_post/<post_id>", methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_by_id(post_id)
    post.delete_instance()
    return "Timeline post deleted successfully"

@app.route('/timeline')
def timeline():
    return render_template('timelines.html', title="Timeline")