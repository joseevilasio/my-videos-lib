from flask import Flask, g
from db import conn
import json
import sqlite3

app = Flask(__name__)


DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect("database.db").cursor()    
    return conn


@app.route("/")
def hello():    
    return "<strong>REST API - MyVideosRepo</strong>"


@app.route("/videos")
def list_all(post_id=None):
    
    cursor = get_db_connection() 
    fields = ("id", "title", "description", "url")
    results = cursor.execute("SELECT * FROM video;")        
    return [dict(zip(fields, video)) for video in results]


@app.route("/videos/<int:video_id>")
def list_one(video_id):
    
    cursor = get_db_connection() 
    fields = ("id", "title", "description", "url")
    results = cursor.execute(f"SELECT * FROM video WHERE id = {video_id};")        
    return [dict(zip(fields, video)) for video in results]

    
