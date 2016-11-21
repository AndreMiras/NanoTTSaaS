import os
import unittest
import webapp


class WebappTestCase(unittest.TestCase):

    def setUp(self):
        self.app = webapp.app.test_client()

    def tearDown(self):
        pass

    def test_home(self):
        """
        Very simple home test case.
        Simply verifies the status code is OK.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
