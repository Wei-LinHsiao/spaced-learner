import unittest

import app

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """
        Tests if flask is running and set up correctly.
        """
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
