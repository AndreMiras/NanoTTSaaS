import json
import webapp
import unittest


class WebappTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = webapp.app.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        """
        Very simple home test case.
        Simply verifies the status code is OK.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api(self):
        """
        Simple API test cases.
        1) minimal test case, just sending a text to the API
        2) asking for audio file address rather than content
        """
        api_url = '/api'
        # 1) minimal test case, just sending a text to the API
        data = {"text": "Test text"}
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "audio/x-wav")
        # 2) asking for audio file address rather than content
        data = {
            "text": "Test text",
            "response_type": "audio_address",
        }
        response = self.client.post(api_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        json_response = json.loads(response.get_data(as_text=True))
        # they audio_file key, contains the file address
        self.assertTrue('audio_file' in json_response)


if __name__ == '__main__':
    unittest.main()
