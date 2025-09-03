import base64
import io
import wave
import requests
from flask import Flask, request, jsonify

db_service_url = "http://localhost:4000/db/catalogue" 
app = Flask(__name__)

@app.route("/catalogue/<string:song>", methods=["PUT"])
def add_track(song):
    js = request.get_json()

    if not js or "song" not in js or "artist" not in js or "full_audio" not in js:
        return "", 400 # Bad request
    
    if not is_valid_audio(js["full_audio"]):
        return "", 415 # Invalid audio
    
    check_rsp = requests.get(f"{db_service_url}/{song}")  
    if check_rsp.status_code == 200:  
        return "", 409 # Conflict

    rsp = requests.post(db_service_url, json=js)
    return "", rsp.status_code

@app.route("/catalogue/<string:song>", methods=["GET"])
def get_track(song):
    rsp = requests.get(f"{db_service_url}/{song}")
    if rsp.status_code == 404:
        return "", 404 # Track not found
    return rsp.json(), rsp.status_code

@app.route("/catalogue", methods=["GET"])
def list_tracks():
    try:
        rsp = requests.get(db_service_url)
        tracks = rsp.json()
        return tracks, rsp.status_code
    
    except requests.exceptions.ConnectionError:
        return "", 503

@app.route("/catalogue/<string:song>", methods=["DELETE"])
def delete_track(song):
    if not song.strip():  
        return "", 400  # Bad Request

    try:
        rsp = requests.delete(f"{db_service_url}/{song}")

        if rsp.status_code == 404:  
            return "", 404 # Track not found
        elif rsp.status_code == 204:  
            return "", 204  # No Content
        else:
            return "", rsp.status_code

    except requests.exceptions.ConnectionError:
        return "", 503

@app.route("/catalogue/clear", methods=["DELETE"])
def clear_catalogue():
    rsp = requests.delete("http://localhost:4000/db/catalogue/clear")  
    return "", rsp.status_code

def is_valid_audio(base64_audio):
    try:
        audio_data = base64.b64decode(base64_audio)
        with wave.open(io.BytesIO(audio_data), "rb") as wav_file:
            return True  

    except (base64.binascii.Error, wave.Error):
        return False 

if __name__ == "__main__":
    app.run(host="localhost", port=3000)