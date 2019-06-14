from flask import Flask, render_template, request

app = Flask(__name__)

# Global variables
if True:
    ## Generate the webpage
    ## DB Schema:
    # u_id - user id
    # e_id - entry id
    # color - color of selected note
    # text - text of entry
    # priority - importance (top five selected on first generation)
    # status - integer from 0 to 4
    # 0 - Not currently selected
    # 1 - Selected, but unanswered
    # 2 - Selected, red
    # 3 - Selected, grey
    # 4 - Selected, green
    # time - timestamp of last called (should be in user, if 24 hours, then change)
    # For now, put in time as have not implemented user

    d1 = dict(
        u_id=0,
        e_id=0,
        color="blue",
        text="Apples",
        priority=1,
        status=0,
        time=0
    )

    d2 = dict(
        u_id=0,
        e_id=1,
        color="",
        text="Oranges",
        priority=1,
        status=0,
        time=0
    )

    d3 = dict(
        u_id=0,
        e_id=2,
        color="blue",
        text="Pears",
        priority=1,
        status=0,
        time=0
    )

    d4 = dict(
        u_id=0,
        e_id=3,
        color="blue",
        text="Mangoes",
        priority=1,
        status=0,
        time=0
    )

    d5 = dict(
        u_id=0,
        e_id=4,
        color="blue",
        text="Blueberries",
        priority=1,
        status=0,
        time=0
    )

    # Mock db of all entires; list for now
    all_entries = [d1, d2, d3, d4, d5]
    current_entries = []

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

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        request_dict = request.form.to_dict()
        # Get the key value of the id, both values are strings
        color = list(request_dict)[0]

        # Go on to next day and process if submit
        if color == "submit":
            start_day()
        # Modify status based on button press
        else:
            # Get color, and modify accordingly
            id = int(request_dict[color])

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
