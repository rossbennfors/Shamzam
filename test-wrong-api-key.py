import base64
import unittest
import requests

recognize_url = "http://localhost:3001/recognize"
catalogue_url = "http://localhost:3000/catalogue"
clear_url = f"{catalogue_url}/clear"

class TestRecognizeEndpoint(unittest.TestCase):
    ########################################################
    ## Turn audDio.py off and set a wrong key before test ##
    ########################################################
    def test_invalid_api_key(self):
        with open("./~Blinding Lights.wav", "rb") as f:
            snippet_audio_data = base64.b64encode(f.read()).decode("ascii")

        hdrs = {"Content-Type": "application/json"}
        js = {
            "audio": snippet_audio_data
            }

        rsp = requests.post(recognize_url, json=js, headers=hdrs)

        self.assertEqual(rsp.status_code, 401)

if __name__ == "__main__":
    unittest.main()