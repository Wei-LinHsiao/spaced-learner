from flask import Flask, render_template, request
import leitner_boxes

app = Flask(__name__)

# Global variables.
current_box = leitner_boxes.BoxSet(0)
debug = True

# Mock db of all entires; list for now.
if debug:
    current_box.create_entry("One", "")
    current_box.create_entry("Two", "")
    current_box.create_entry("Three", "")
    current_box.create_entry("Four", "")
    current_box.create_entry("Five", "")
    current_box.create_entry("Six", "")
    current_box.create_entry("Seven", "")

# Updates all entries, given the status of their info.
def start_day():
    ## This code is at the start of a "day"; sort and figure things out
    # Look at current_entries and modify the status of all_entries by status
    for entry in current_box.get_all_cards():
        # Red
        if entry.status == 2:
            # Lower priority value; want to see soon
            current_box.downgrade_entry(entry)
        # Grey
        elif entry.status == 3:
            # Do nothing
            entry.status = 3
        # Green
        elif entry.status == 4:
            current_box.upgrade_entry(entry)
        entry.status = 0

    # Advance the day.
    current_box.cur_day += 1
# General Functions

## Route Functions: Render main pages.
@app.route('/tester', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def tester():
    if request.method == "POST":
        # If is submit, next day and end.
        if "submit" in request.form:
            start_day()
        else:
            print(request.json)
            # Get color, and modify accordingly
            id = int(request.json["e_id"])
            entry = current_box.get_entry(id)
            color = request.json["color"]

            # # Update color and status values
            # # Don't change priority if status is not 1
            # # Return value to normal if status is already that color
            cur_status = entry.status
            if color == "red":
                if cur_status != 2:
                    entry.status = 2
                else:
                    entry.status = 1
            if color == "grey":
                if cur_status != 3:
                    entry.status = 3
                else:
                    entry.status = 1
            if color == "green":
                if cur_status != 4:
                    entry.status = 4
                else:
                    entry.status = 1

    return render_template('tester.html', entries = current_box.get_current_cards())

# Run this code before Flask starts
start_day()

if __name__ == '__main__':
    app.run()
