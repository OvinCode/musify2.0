from flask import Flask, render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import base64
from requests import post
import json

app = Flask(__name__)

#database connection
app.config['MONGO_URI'] = 'mongodb+srv://maybeovin:Ovin_9039@firstcluster.ul9odhi.mongodb.net/'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.allsongs

load_dotenv()

#loading spotifywebapi credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {'grant-type': "authorization_code"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()
print(token)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form') 
def form():
    return render_template('form.html')

@app.route('/handle_click', methods=['POST'])
def handle_click():
    # Perform server-side actions here
    # You can return a response if needed
    artist = request.form.get('artist')
    title = request.form.get('title')

    # Create a new song document
    new_song = {'artist': artist, 'title': title}

    # Insert the new song into the MongoDB collection
    db.songs.insert_one(new_song)
    return render_template("success.html")

@app.route('/add_song')
def add():
    new_song = {'artist': 'Anjan Dutta', 'title': 'roma'}
    db.songs.insert_one(new_song)
    return 'Song added successfully!'

@app.route('/remove_song')
def remove():
    return 'Hello, Flask!'

@app.route('/play_song')
def get_artist():




    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)
