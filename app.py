from flask import Flask, render_template,request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import base64
from requests import post,get
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
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {'grant_type': "client_credentials",
            'client_id' :client_id,
             'client_secret' :client_secret,}
    
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result["access_token"]
    return token


def get_artist(artist):
    token = get_token() 
    url_artist ='https://api.spotify.com/v1/search?q='+ artist +'&type=artist&market=IN&offset=0'
    headers = {
        "Authorization": "Bearer " + token,
    }
    result = get(url_artist, headers=headers)
    json_result = result.json()

    artists = json_result.get('artists', {}).get('items', [])
    return artists


@app.route('/search', methods=['POST'])
def search_artist():
    search_artist = request.form.get('search')
    artists = get_artist(search_artist)
    return render_template('artists.html', artists=artists)
    


@app.route('/artist/<artist_id>')
def get_albums(artist_id):
    token = get_token()
    url_albums = "https://api.spotify.com/v1/artists/"+ artist_id + "/albums"
    headers = {
        "Authorization": "Bearer " + token,
    }
    result = get(url_albums, headers=headers)
    json_result = result.json()

    albums = json_result.get('items', [])
    return render_template('artist_details.html', albums=albums)


@app.route('/album/<album_id>')
def get_tracks(album_id):
    token = get_token()
    url_albums = "https://api.spotify.com/v1/albums/"+ album_id + "/tracks"
    headers = {
        "Authorization": "Bearer " + token,
    }
    result = get(url_albums, headers=headers)
    json_result = result.json()

    tracks = json_result.get('items', [])
    return render_template('album_details.html', tracks=tracks)

@app.route('/')
def index():
    return render_template('index1.html')

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



if __name__ == '__main__':
    app.run(debug=True)
