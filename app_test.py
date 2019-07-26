import unittest
# import app
import leitner_boxes

class FlaskAppCases(unittest.TestCase):

    def test_index(self):
        """
        Tests if flask is running and set up correctly.
        """
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class LeitnerBoxesBoxCases(unittest.TestCase):
    def setUp(self):
        self.entry_1 = leitner_boxes.Entry(0, 0, "", "")
        self.entry_2 = leitner_boxes.Entry(0, 1, "", "")
        self.entry_3 = leitner_boxes.Entry(0, 2, "", "")

        self.box = leitner_boxes.Box(0, 0)

    def test_box_entry_add(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")

    def test_box_entry_remove(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_2)
        self.box.remove_entry(self.entry_1)
        self.assertEqual(self.box.get_size(), 1, "Box is not of expected size")

    def test_box_get_all(self):
        self.box.add_entry(self.entry_1)
        self.box.add_entry(self.entry_2)
        all = self.box.get_all_entries()

        self.assertEqual(type(all[0]), type(self.entry_1))
        self.assertEqual(len(all), 2)

class LeitnerBoxesLevelCases(unittest.TestCase):
    def setUp(self):
        self.entry_1 = leitner_boxes.Entry(0, 0, "", "")
        self.entry_2 = leitner_boxes.Entry(0, 1, "", "")
        self.entry_3 = leitner_boxes.Entry(0, 2, "", "")

        self.box = leitner_boxes.Box(0, 0)
        self.level = leitner_boxes.Level(0, 3)

    def test_level_add(self):
        self.level.add_entry(0, self.entry_1)
        self.assertTrue(self.level.get_size() == 1)

        self.level.add_entry(1, self.entry_2)
        self.assertTrue(self.level.get_size() == 2)

        self.level.add_entry(2, self.entry_3)
        self.assertTrue(self.level.get_size() == 3)

        # Make sure that entries have properly updated box numbers.
        self.assertTrue(self.entry_1.box == 0, "Entry has incorrect box number!")
        self.assertTrue(self.entry_2.box == 1, "Entry has incorrect box number!")
        self.assertTrue(self.entry_3.box == 2, "Entry has incorrect box number!")

    def test_level_remove(self):
        self.level.add_entry(0, self.entry_1)
        self.level.remove_entry(self.entry_1)
        self.assertTrue(self.level.get_size() == 0)

    def test_level_balancer(self):
        self.level.add_entry_balanced(self.entry_1)
        self.level.add_entry_balanced(self.entry_2)
        self.level.add_entry_balanced(self.entry_3)

        # Make sure the three levels are balanced.
        boxes = list(map(lambda x: x.get_size(), self.level.boxes))

        self.assertTrue(boxes[0] == boxes[1] and
                        boxes[1] == boxes[2] and
                        boxes[0] == boxes[2], "Distribution is not even!")

    def test_level_get_all(self):
        self.level.add_entry_balanced(self.entry_1)
        self.level.add_entry_balanced(self.entry_2)
        self.level.add_entry_balanced(self.entry_3)

        all = list(self.level.get_all_entries())

        # Ensure Length is correct, all elements are in.
        self.assertEqual(len(all), 3)

        # Ensure type is correct, all elements are entries.
        for i in all:
            self.assertEqual(type(i), type(self.entry_1))

class LeitnerBoxesDeckCases(unittest.TestCase):
    def setUp(self):
        self.entry_1 = leitner_boxes.Entry(0, 0, "", "")
        self.entry_2 = leitner_boxes.Entry(0, 1, "", "")
        self.entry_3 = leitner_boxes.Entry(0, 2, "", "")

        self.box = leitner_boxes.Box(0, 0)
        self.level = leitner_boxes.Level(0, 3)
        self.deck = leitner_boxes.BoxSet(0)

    def test_deck_create_entry(self):
        self.deck.create_entry("", "")
        self.assertTrue(self.deck.get_size() == 1)
        self.deck.create_entry("", "")
        self.assertTrue(self.deck.get_size() == 2)

    def test_deck_remove(self):
        entry_1 = self.deck.create_entry("", "")
        entry_2 = self.deck.create_entry("", "")
        self.assertTrue(self.deck.get_size() == 2)
        self.deck.remove_entry(entry_1)
        self.assertTrue(self.deck.get_size() == 1)

    def test_deck_get_entry(self):
        for i in range(0, 10):
            self.deck.create_entry("", "")

        for i in range(0, 10):
            self.assertEqual(self.deck.get_entry(i).e_id, i)

    def test_deck_upgrade_one(self):
        # Upgrade the deck; ensure it is in deck two.
        entry_1 = self.deck.create_entry("", "")
        entry_2 = self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.upgrade_entry(entry_1)
        self.deck.upgrade_entry(entry_2)

        # Ensure that level two is of size two.
        self.assertTrue(self.deck.levels[1].get_size() == 2)

    def test_deck_upgrade_multiple(self):
        entry_1 = self.deck.create_entry("", "")
        entry_2 = self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.upgrade_entry(entry_1)
        self.deck.upgrade_entry(entry_2)
        self.deck.upgrade_entry(entry_1)
        self.deck.cur_day = 12
        self.deck.upgrade_entry(entry_2)

        # Ensure that level three is of size two.
        self.assertTrue(self.deck.levels[2].get_size() == 2)

        # Ensure that entries are in correct box.
        # entry_1 was upgraded on day 0; should be in box 0.
        # entry_2 was upgraded on day 12 in an interval of five days; should be in box 2.
        self.assertTrue(entry_1.box == 0)
        self.assertTrue(entry_2.box == 2)
        return

    def test_deck_upgrade_finish(self):
        entry_1 = self.deck.create_entry("", "")
        for i in range(0, 5):
            self.deck.upgrade_entry(entry_1)

        assert(entry_1.level == 5)

        with self.assertRaises(Exception):
            self.deck.upgrade_entry(entry_1)

    def test_deck_downgrade_one(self):
        # Upgrade the deck; ensure it is in deck two.
        entry_1 = self.deck.create_entry("", "")
        entry_2 = self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.create_entry("", "")
        self.deck.upgrade_entry(entry_1)
        self.deck.upgrade_entry(entry_2)
        self.deck.upgrade_entry(entry_2)
        self.deck.upgrade_entry(entry_2)

        # Ensure that downgrading results it in going to 0.
        self.deck.downgrade_entry(entry_1)
        self.deck.downgrade_entry(entry_2)
        print(self.deck)
        self.assertTrue(self.deck.levels[0].get_size() == 4)
        self.assertTrue(self.deck.levels[1].get_size() == 0)


    def test_deck_get_all(self):
        for i in range(0, 100):
            entry = self.deck.create_entry("", "")

            if i % 2 == 0:
                self.deck.upgrade_entry(entry)
            if i % 3 == 0:
                self.deck.upgrade_entry(entry)
            if i % 5 == 0:
                self.deck.upgrade_entry(entry)
            if i % 7 == 0:
                self.deck.upgrade_entry(entry)

            self.deck.cur_day += 1

        all = self.deck.get_all_cards()
        self.assertEqual(len(all), 100)

        # Check if types are equal.
        for i in all:
            self.assertEqual(type(i), type(self.entry_1))

    # Tests of get_current gets a list of entries.
    def test_deck_get_current(self):
        for i in range(0, 100):
            entry = self.deck.create_entry("", "")

            if i % 2 == 0:
                self.deck.upgrade_entry(entry)
            if i % 3 == 0:
                self.deck.upgrade_entry(entry)
            if i % 5 == 0:
                self.deck.upgrade_entry(entry)
            if i % 7 == 0:
                self.deck.upgrade_entry(entry)

            self.deck.cur_day += 1

        all = self.deck.get_current_cards()

        # Ensures that typing is correct.
        for i in all:
            self.assertEqual(type(i), type(self.entry_1))

if __name__ == '__main__':
    unittest.main()
