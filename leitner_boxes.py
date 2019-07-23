# TODO: Add functions to change values in server.
class Entry:
    def __init__(self, u_id, e_id, front_text, back_text):
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
        self.u_id = u_id
        self.e_id = e_id
        self.front_text = front_text
        self.back_text = back_text
        self.status = 0
        self.level = 0
        self.box = 0

    # Tostring method; simply return the string's eid. May update.
    def __str__(self):
        return str(self.e_id)

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

    # Adds entry in box.
    def add_entry(self, entry):
        self.box[entry.e_id] = entry
        entry.box = self.num
        entry.level = self.level

    # Removes entry, if it exists in box.
    def remove_entry(self, e_id):
        if e_id in self.box:
            del self.box[e_id]
        else:
            # Throw error.
            raise KeyError("No entry with e_id " + str(e_id) +
                           " found in box " + str(self.num) +
                           " at level " + str(self.level))

# One Leitner level.
class Level(object):
    def __init__(self, level):
        self.level = level
        # Initiate a number of boxes, relative to level value.
        self.boxes = [Box(level, i) for i in range(0, level)]
        self.finished = False

    def __str__(self):
        level_str = "Level " + str(self.level) + ":"
        boxes_str = "\n  ".join(map(str, self.boxes))

        return("\n  ".join([level_str, boxes_str]))

    # Adds an entry to a box.
    def add_entry(self, box, entry):
        self.boxes[box].add_entry(entry)

    # Adds an entry to a level in a balanced manner.
    def add_entry_balanced(self, entry):
        min_box = min(self.boxes, key = lambda x: x.get_size())
        min_box.add_entry(entry)

    # Removes an entry in a certain box.
    def remove_entry(self, box, e_id):
        self.boxes[box].remove_entry(e_id)

    # If too unbalanced, rebalances boxes to be more even.
    # TODO: Implement
    def rebalance(self):
        return

# A Leitner level representing the final level.
class FinishedLevel(object):
    def __init__(self):
        # None represents the last level.
        self.level = None
        # Initiate a number of boxes, relative to level value.
        self.boxes = [Box()]
        self.finished = True

    # Adds an entry to a box.
    def add_entry(self, box, entry):
        self.boxes[0].add_entry(entry)

    # Adds an entry to a level in a balanced manner.
    def add_entry_balanced(self, entry):
        self.add_entry(entry)

    # Removes an entry in a certain box.
    def remove_entry(self, box, e_id):
        self.boxes[0].remove_entry(e_id)

    # If too unbalanced, rebalances boxes to be more even.
    def rebalance(self):
        return

# One set of Leitner Boxes, with all levels.
class BoxSet(object):
    # Hardcode the progression; 1, 2, 5, 8, 14, NONE.
    def __init__(self, u_id):
        self.u_id = u_id
        self.cur_day = 0
        self.next_eid = 0

        # Initiate a number of boxes, relative to level value.
        self.levels = []
        self.levels.append(Level(1))
        self.levels.append(Level(2))
        self.levels.append(Level(5))
        self.levels.append(Level(8))
        self.levels.append(Level(14))
        self.levels.append(FinishedLevel())

        self.num_levels = len(self.levels) - 1

    # Creates a new entry, and puts it in the first Leitner box
    def create_entry(self, front_text, back_text):
        new_entry = Entry(self.u_id, self.next_eid, front_text, back_text)
        self.next_eid += 1
