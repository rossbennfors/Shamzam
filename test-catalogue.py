import requests
import unittest
import base64

catalogue_url = "http://localhost:3000/catalogue"

class Testing(unittest.TestCase):
    def setUp(self):
        requests.delete(f"{catalogue_url}/clear")
    
    # Helper function to add a test track to the catalogue
    def add_test_track(self, song="Blinding Lights", artist="The Weeknd", file_path="./Blinding Lights.wav"):
        with open(file_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode("ascii")

        hdrs = {"Content-Type": "application/json"}
        js = {"song": song, "artist": artist, "full_audio": audio_data}
        rsp = requests.put(f'{catalogue_url}/{song}', headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 201)
    
    # User Story 1 Tests
    def test_add_track(self):
        self.add_test_track()

    def test_add_track_invalid_audio(self):
        song = "Blinding Lights"
        artist = "The Weeknd"
        invalid_audio = "thisisnotbase64encodeddata"

        js = {"song": song, "artist": artist, "full_audio": invalid_audio}
        rsp = requests.put(f"{catalogue_url}/{song}", json=js)

        self.assertEqual(rsp.status_code, 415)
    
    def test_add_duplicate_track(self):
        self.add_test_track()
        song = "Blinding Lights"
        artist = "The Weeknd"
        with open("./Blinding Lights.wav", "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode("ascii")

        hdrs = {"Content-Type": "application/json"}
        js = {"song": song, "artist": artist, "full_audio": audio_data}
        rsp = requests.put(f'{catalogue_url}/{song}', headers=hdrs, json=js)

        self.assertEqual(rsp.status_code, 409)
    
    # User Story 2 Tests
    def test_delete_existing_track(self):
        self.add_test_track()

        rsp = requests.delete(f'{catalogue_url}/Blinding Lights')
        self.assertEqual(rsp.status_code, 204)

        rsp = requests.get(f'{catalogue_url}/Blinding Lights')
        self.assertEqual(rsp.status_code, 404)
    
    def test_delete_nonexistent_track(self):
        song = "Nonexistent Song"
        rsp = requests.delete(f'{catalogue_url}/{song}')
        self.assertEqual(rsp.status_code, 404)  

    def test_delete_invalid_track_name(self):
        invalid_song = "  " 
        rsp = requests.delete(f'{catalogue_url}/{invalid_song}')
        self.assertEqual(rsp.status_code, 400)  
    
    # User Story 3 Tests
    def test_list_tracks(self):
        self.add_test_track()
        rsp = requests.get(catalogue_url)
        self.assertEqual(rsp.status_code, 200)

        tracks = rsp.json()
        self.assertIn({"song": "Blinding Lights", "artist": "The Weeknd"}, tracks)
    
if __name__ == "__main__":
    unittest.main()
