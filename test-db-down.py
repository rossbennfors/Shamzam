import requests
import unittest

catalogue_url = "http://localhost:3000/catalogue"

class Testing(unittest.TestCase):
    ##############################################
    ## Turn database_service.py off before test ##
    ##############################################
    def test_db_down_with_delete(self):
        rsp = requests.delete(f'{catalogue_url}/Blinding Lights')
        self.assertEqual(rsp.status_code, 503)

    def test_db_down_with_list_tracks(self):
        rsp = requests.get(catalogue_url)
        self.assertEqual(rsp.status_code, 503)

if __name__ == "__main__":
    unittest.main()