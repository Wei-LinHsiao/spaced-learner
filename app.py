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
    for i in range(0, len(current_entries)):
        status = current_entries[i]["status"]

        # Red
        if status == 2:
            # Lower priority value; want to see soon
            all_entries[i]["priority"] = all_entries[i]["priority"]  * 0.25 - 5
        # Grey
        elif status == 3:
            # Add to priority: Can see soon
            all_entries[i]["priority"] = all_entries[i]["priority"]  * 0.25 + 2
        # Green
        elif status == 4:
            # Add to priority: Can see soon
            all_entries[i]["priority"] = all_entries[i]["priority"]  * 0.25 + 5

    # Sort entires by priority before rendering
    all_entries.sort(key=lambda x: x["priority"])

    # Clear current entries, and get the top three overall entries
    # Need to check for case where < 3 entries
    # Change their statuses to 1 to indicate usage
    del current_entries[0:len(current_entries)]
    current_entries.extend(all_entries[0:3])

    for i in range(0, 3):
        current_entries[i]["status"] = 1

# General Functions

## Route Functions: API endpoints.
@app.route('/entry/tes', methods=["GET", "POST"])


## Route Functions: Render main pages.
@app.route('/tester', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def tester():
    if request.method == "POST":
        # If is submit, next day and end.
        if "submit" in request.form:
            start_day()
        else:
            # Get color, and modify accordingly
            id = int(request.json["e_id"])
            color = request.json["color"]

            # Change the priority of our current entry
            # Get id of current entry
            for i in range(0, len(current_entries)):
                if current_entries[i]["e_id"] == id:
                    id_idx = i

            # Update color and status values
            # Don't change priority if status is not 1
            # Return value to normal if status is already that color
            cur_status = current_entries[id_idx]["status"]
            if color == "red":
                if cur_status != 2:
                    current_entries[id_idx]["status"] = 2
                else:
                    current_entries[id_idx]["status"] = 1
            if color == "grey":
                if cur_status != 3:
                    current_entries[id_idx]["status"] = 3
                else:
                    current_entries[id_idx]["status"] = 1
            if color == "green":
                if cur_status != 4:
                    current_entries[id_idx]["status"] = 4
                else:
                    current_entries[id_idx]["status"] = 1

    return render_template('tester.html', entries = current_entries)

# Run this code before Flask starts
start_day()

if __name__ == '__main__':
    app.run()
