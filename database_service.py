from flask import Flask, request, jsonify
import repository

app = Flask(__name__)
db = repository.Repository("tracks")

@app.route("/db/catalogue", methods=["GET"])
def list_tracks():
    tracks = db.get_all_tracks()
    return jsonify(tracks), 200

@app.route("/db/catalogue/<string:song>", methods=["GET"])
def get_track(song):
    track = db.get_track_with_audio(song)
    if track:
        return jsonify(track), 200
    return "", 404 

@app.route("/db/catalogue", methods=["POST"])
def add_track():
    js = request.get_json()
    if db.insert(js):
        return "", 201  
    return "", 500 

@app.route("/db/catalogue/<string:song>", methods=["DELETE"])
def delete_track(song):
    if db.lookup(song):
        db.delete(song)
        return "", 204  
    return "", 404

@app.route("/db/catalogue/clear", methods=["DELETE"])
def clear_database():
    db.clear()
    return "", 204 

if __name__ == "__main__":
    app.run(host="localhost", port=4000) 