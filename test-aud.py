import base64
import unittest
import requests

recognize_url = "http://localhost:3001/recognize"
catalogue_url = "http://localhost:3000/catalogue"
clear_url = f"{catalogue_url}/clear"

class TestRecognizeEndpoint(unittest.TestCase):
    def setUp(self):
        requests.delete(clear_url)

    def test_recognize_and_get_full_track(self):
        song = "Blinding Lights"
        artist = "The Weeknd"
        with open("./Blinding Lights.wav", "rb") as f:
            full_audio_data = base64.b64encode(f.read()).decode("ascii")

        hdrs = {"Content-Type": "application/json"}
        track_js = {"song": song, "artist": artist, "full_audio": full_audio_data}
        rsp = requests.put(f"{catalogue_url}/{song}", headers=hdrs, json=track_js)

        self.assertEqual(rsp.status_code, 201)

        with open("./~Blinding Lights.wav", "rb") as f:
            snippet_audio_data = base64.b64encode(f.read()).decode("ascii")

        snippet_js = {"audio": snippet_audio_data}
        rsp = requests.post(recognize_url, json=snippet_js, headers=hdrs)

        self.assertEqual(rsp.status_code, 200)
        song_data = rsp.json()
        audio_binary = base64.b64decode(song_data["full_audio"])
        audio_name = song_data["song"] + "_full.wav"
        with open(audio_name, "wb") as f:
            f.write(audio_binary)

    def test_recognize_invalid_audio_format(self):
        invalid_audio = "invalid audio"

        hdrs = {"Content-Type": "application/json"}
        js = {"audio": invalid_audio}
        rsp = requests.post(recognize_url, json=js, headers=hdrs)
        print(rsp.text)
        self.assertEqual(rsp.status_code, 415)
    
    def test_song_not_in_catalogue(self):
        with open("./~good 4 u.wav", "rb") as f:
            snippet_audio_data = base64.b64encode(f.read()).decode("ascii")
        hdrs = {"Content-Type": "application/json"}
        snippet_js = {"audio": snippet_audio_data}
        rsp = requests.post(recognize_url, json=snippet_js, headers=hdrs)

        self.assertEqual(rsp.status_code, 404)

if __name__ == "__main__":
    unittest.main()