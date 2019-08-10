from functools import reduce
from app import db
from app.models import Deck as DBDeck
from app.models import Entry as DBEntry

# TODO: Add functions to change values in server.
class Entry:
    def __init__(self, u_id, deck_id, front_text, back_text, push_db=True):
        # All Entries have the following properties:
            # u_id - user id
            # e_id - entry id
            # front_text - main text of entry
            # back_text - secondary text
            # status - integer from 0 to 4
                # 0 - Not currently selected
                # 1 - Selected, but unanswered
                # 2 - Selected, red
                # 3 - Selected, grey
                # 4 - Selected, green
            # level, box - Leitner method boxes.
        self.id = None
        self.u_id = u_id
        # Should this be the deckID?
        self.deck_id = deck_id
        self.front_text = front_text
        self.back_text = back_text
        # Changing info
        self.level = 0
        self.box = 0
        self.status = 0

        if push_db:
            db_entry = DBEntry(u_id = self.u_id,
                               deck_id = self.deck_id,
                               box = self.box,
                               level = self.level,
                               front_text = self.front_text,
                               back_text = self.back_text)
            db.session.add(db_entry)
            db.session.commit()

            # Set the current deck_id. Deck_id's are unique.
            db.session.flush()
            self.id = db_entry.id


    # Tostring method; simply return the string's eid. May update.
    def __str__(self):
        return str(self.id)

# One Leitner flashcard box.
class Box(object):
    def __init__(self, level, num):
        # All items in box.
        # Stored in memory as an entry that is indexed by entry id.
        self.box = {}
        self.level = level
        self.num = num

    # Tostring method: return the box number (but not level).
    def __str__(self):
        return "Box " + str(self.num) + " - " + str(list(self.box.keys()))

    def get_size(self):
        return len(self.box)

    def get_all_entries(self):
        return list(self.box.values())

    # Adds entry in box.
    def add_entry(self, entry):
        self.box[entry.id] = entry
        entry.box = self.num
        entry.level = self.level

    # Removes entry, by entry_id, if it exists in box.
    def remove_entry(self, entry):
        if entry.id in self.box:
            del self.box[entry.id]
        else:
            # Throw error.
            raise KeyError("No entry with e_id " + str(entry.id) +
                           " found in box " + str(self.num) +
                           " at level " + str(self.level))

# One Leitner level.
class Level(object):
    def __init__(self, level, interval):
        self.level = level
        self.interval = interval
        # Initiate a number of boxes, relative to level value.
        self.boxes = [Box(self.level, i) for i in range(0, interval)]
        self.finished = False

    def __str__(self):
        level_str = "Level " + str(self.level) + ":"
        boxes_str = "\n  ".join(map(str, self.boxes))

        return("\n  ".join([level_str, boxes_str]))

    def get_size(self):
        return sum(list(map(lambda x: x.get_size(), self.boxes)))

    # Returns an iterable (to avoid copying lists) of all entries.
    def get_all_entries(self):
        return reduce(list.__add__, map(lambda x: x.get_all_entries(), self.boxes))

    # Adds an entry to a box.
    def add_entry(self, box, entry):
        self.boxes[box].add_entry(entry)

    # Adds an entry to a level in a balanced manner.
    def add_entry_balanced(self, entry):
        min_box = min(self.boxes, key=lambda x: x.get_size())
        min_box.add_entry(entry)

    # Removes an entry in a certain box with a given e_id.
    def remove_entry(self, entry):
        self.boxes[entry.box].remove_entry(entry)

    # If too unbalanced, rebalances boxes to be more even.
    # TODO: Implement
    def rebalance(self):
        return

# A Leitner level representing the final level.
class FinishedLevel(object):
    def __init__(self, level):
        # None represents the last level.
        self.level = level
        self.interval = 0
        # Initiate a number of boxes, relative to level value.
        self.boxes = [Box(5, 0)]
        self.finished = True

    def __str__(self):
        level_str = "Archive :"
        boxes_str = "\n  ".join(map(str, self.boxes))
        return("\n  ".join([level_str, boxes_str]))

    def get_size(self):
        return self.boxes[0].get_size()

    def get_all_entries(self):
        return reduce(list.__add__, map(lambda x: x.get_all_entries(), self.boxes))

    # Adds an entry to a box.
    def add_entry(self, box, entry):
        self.boxes[0].add_entry(entry)

    # Adds an entry to a level in a balanced manner.
    def add_entry_balanced(self, entry):
        self.add_entry(entry)

    # Removes an entry in a certain box.
    def remove_entry(self, entry):
        self.boxes[entry.box].remove_entry(entry)

    # If too unbalanced, rebalances boxes to be more even.
    def rebalance(self):
        return

# One set of Leitner Boxes, with all levels.
class BoxSet(object):
    # Hardcode the progression; 1, 2, 5, 8, 14, NONE.
    def __init__(self, u_id, name = "Untitled Box", push_db = True):
        # Unique identifier for deck.
        self.deck_id = None
        self.u_id = u_id
        self.cur_day = 0
        self.name = name

        # Initiate a number of boxes, relative to level value.
        self.levels = [
            Level(0, 1),
            Level(1, 2),
            Level(2, 5),
            Level(3, 8),
            Level(4, 14),
            FinishedLevel(5)
        ]

        self.entries = {}
        self.num_levels = len(self.levels) - 1

        # Add a box to the DB.
        if push_db:
            db_deck = DBDeck(u_id = self.u_id, name = self.name)
            db.session.add(db_deck)
            db.session.commit()

            # Set the current deck_id. Deck_id's are unique.
            db.session.flush()
            self.deck_id = db_deck.id

    def __str__(self):
        deck_str = "Deck id " + str(self.deck_id) + ":"
        level_str = "\n  ".join(map(lambda x: str(x).replace("  ", "    "), self.levels))

        return("\n  ".join([deck_str, level_str]))

    # Creates a new entry, and puts it in the first Leitner box
    def create_entry(self, front_text, back_text):
        new_entry = Entry(self.u_id, self.deck_id, front_text, back_text)
        self.add_entry(0, 0, new_entry)
        self.entries[new_entry.id] = new_entry
        return new_entry

    # Gets an entry by its e_id.
    def get_entry(self, id):
        return self.entries[id]

    # Adds entry to a given level and box.
    def add_entry(self, level, box, entry):
        self.levels[level].add_entry(box, entry)

    # Adds entry to a given level in a balanced manner.
    def add_entry_balanced(self, level, entry):
        self.levels[level].add_entry_balanced(entry)

    # Remove an entry from its level and box.
    def remove_entry(self, entry):
        self.levels[entry.level].remove_entry(entry)

    def upgrade_entry(self, entry):
        # If it is in 1, upgrade in a balanced fashion.
        # If final level, throw error.
        if entry.level == 5:
            raise AssertionError("Entries that are at max level should not be updated!")
        # Remove from current level.
        self.remove_entry(entry)

        if entry.level == 0:
            # Move to next level in balanced fashion.
            self.levels[1].add_entry_balanced(entry)
        elif entry.level in range(1, 4):
            # Move to next level in unbalanced fashion.
            next_level = entry.level + 1
            next_box = self.cur_day % self.levels[next_level].interval
            self.levels[next_level].add_entry(next_box, entry)
        elif entry.level == 4:
            # Move entry to finished box.
            self.levels[5].add_entry(0, entry)
        elif entry.level == 5:
            # Move entry to finished box.
            raise AssertionError("Entry " + str(entry.id) + " is already archived.")
        else:
            raise AssertionError("Entry " + str(entry.id) + " has an invalid level.")

    def downgrade_entry(self, entry):
        # If it is in 0, do nothing.
        if entry.level == 0:
            return
        # Remove from current level.
        self.remove_entry(entry)
        if entry.level in range(1, 5):
            # Move down to level 0.
            self.levels[0].add_entry_balanced(entry)
        elif entry.level == 5:
            # Move entry to finished box.
            raise AssertionError("Entry " + str(entry.id) + " is already archived.")
        else:
            raise AssertionError("Entry " + str(entry.id) + " has an invalid level.")

    def get_size(self):
        return sum(list(map(lambda x: x.get_size(), self.levels)))

    def get_all_cards(self):
        # Return all entries in all levels in an iterable.
        # We cannot use map; improper iterables.
        return reduce(list.__add__, map(lambda x: x.get_all_entries(), self.levels))

    def get_current_cards(self):
        # Get all cards tested in this day.
        # Functional: Gets box indes that corresponds to the correct day, and gets all entries.
        return reduce(list.__add__, map(lambda i: self.levels[i]
                   .boxes[self.cur_day % self.levels[i].interval]
                   .get_all_entries(), range(0, 5)))