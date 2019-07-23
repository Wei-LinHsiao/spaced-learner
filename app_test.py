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
        self.entry_1 = leitner_boxes.Entry(0, 0, "", "")
        self.entry_2 = leitner_boxes.Entry(0, 1, "", "")
        self.entry_3 = leitner_boxes.Entry(0, 2, "", "")
        self.entry_4 = leitner_boxes.Entry(0, 3, "", "")

        self.box = leitner_boxes.Box(0, 0)

        self.level = leitner_boxes.Level(3)

    def test_box_entry_add(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")

    def test_box_entry_remove(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_2)
        self.box.remove_entry(1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")

    def test_level_addition(self):
        self.level.add_entry(0, self.entry_1)
        self.level.add_entry(1, self.entry_2)
        self.level.add_entry(2, self.entry_3)

        # Make sure that entries have properly updated box numbers.
        self.assertTrue(self.entry_1.box == 0, "Entry has incorrect box number!")
        self.assertTrue(self.entry_2.box == 1, "Entry has incorrect box number!")
        self.assertTrue(self.entry_3.box == 2, "Entry has incorrect box number!")


    def test_level_balancer(self):
        self.level.add_entry_balanced(self.entry_1)
        self.level.add_entry_balanced(self.entry_2)
        self.level.add_entry_balanced(self.entry_3)

        # Make sure the three levels are balanced.
        boxes = list(map(lambda x: x.get_size(), self.level.boxes))

        self.assertTrue(boxes[0] == boxes[1] and
                        boxes[1] == boxes[2] and
                        boxes[0] == boxes[2], "Distribution is not even!")
    

if __name__ == '__main__':
    unittest.main()
