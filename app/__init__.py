"""
This is the flask app
"""
from email.policy import default
import json
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
from app.utilities import md_to_html

load_dotenv()

app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

with open("./app/static/user-template.json", encoding="utf-8") as file:
    user = json.load(file)


@app.route("/")
def index():
    """
    Renders the homepage.
    """

    # ? I'm using some random persons API for preview reasons.
    projects = requests.get(f"https://ghapi.dstn.to/{user['github']}/pinned").json()
    user["about"] = md_to_html(user["about"])
    user["projects"] = projects["data"]

    return render_template("/pages/home.html", user=user)


@app.route("/project/<name>")
def project(name):
    """
    Renders a project page if available.
    """

    # ? We would actually look for the project page in a database.
    # ? For now let's serve this template
    file_path = "./app/static/project-template.md"

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    html = md_to_html(text)

    return render_template("/pages/project.html", user=user, content=html)

@app.errorhandler(404)
def page_not_found(_e):
    """
    Renders a 404 page whenever a user visits an unknown route.
    """
    return render_template("/pages/404.html"), 404

@app.route( '/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route( '/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route( '/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post(id):
    TimelinePost.delete_instance(TimelinePost.get_by_id(id)) 
    return "The post has been deleted"


@app.route('/timeline')
def timeline():
    posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
    return render_template('/pages/timeline.html', title='Timeline', url=os.getenv("URL"), posts=posts)