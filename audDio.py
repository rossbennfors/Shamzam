import base64
import os 
import requests
from flask import Flask, request, jsonify

KEY = os.environ["KEY"] #"b11314e468ee64d3f1fe7f2a9753c611"
api_url = "https://api.audd.io/"
catalogue_url = "http://localhost:3000/catalogue" 

app = Flask(__name__)

@app.route("/recognize",methods=["POST"])
def recognize():
    js = request.get_json()
    audio_snippet = js.get("audio")
    if not is_valid_audio(audio_snippet):
        return "", 415  # Unsupported Media Type

    song_title = identify_song(audio_snippet)
    if isinstance(song_title, tuple) and song_title[1] == 401:
        return "", 401  # Unauthorized
    
    full_audio = get_full_track(song_title)
    if full_audio is None:
        return "", 404  # Not Found in catalogue

    return jsonify({"song": song_title,"full_audio": full_audio}), 200  # OK

def identify_song(audio):
    data = {
        "api_token": KEY,
        "audio": audio,
    }
    rsp = requests.post(api_url,data=data)
    
    if rsp.status_code == 200:
        response_json = rsp.json()
        if response_json.get("status") == "error":
            error_code = response_json.get("error", {}).get("error_code")
            if error_code == 900: # Invalid key code from AudD.io
                return "", 401 
        
        if response_json.get("status") == "success" and response_json.get("result") != None:
            return response_json["result"].get("title")
        
    else:
        return None
    

def get_full_track(song):
    rsp = requests.get(f"{catalogue_url}/{song}")
    if rsp.status_code == 200:
        track_data = rsp.json()
        return track_data.get("full_audio") 
    return None

def is_valid_audio(base64_audio):
    try:
        base64.b64decode(base64_audio, validate=True)
        return True
    except (ValueError, TypeError):
        return False

if __name__ == "__main__":
    app.run(host="localhost",port=3001)