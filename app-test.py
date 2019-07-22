import unittest

import app
import leitner_boxes

class FlaskAppCases(unittest.TestCase):

    def test_index(self):
        """
        Tests if flask is running and set up correctly.
        """
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class LeitnerBoxesCases(unittest.TestCase):
    def setUp(self):
        self.box = leitner_boxes.Box(0, 0)
        self.entry_1 = leitner_boxes.Entry(0, 0, "", "")
        self.entry_2 = leitner_boxes.Entry(0, 1, "", "")

    def test_box_entry_add(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")

    def test_box_entry_remove(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_2)
        self.box.remove_entry(1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")


if __name__ == '__main__':
    unittest.main()
