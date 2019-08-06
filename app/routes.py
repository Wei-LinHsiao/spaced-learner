from flask import render_template, request, flash, redirect
from app import app
from app import current_box
from app.forms import LoginForm

# General Functions
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

## Rotue Functions: API

# Updates a given entry, given an e_id and button color.
@app.route('/api/entry/status-update', methods=["POST"])
def api_entry_status_update():
    if request.method == "POST":
        # Get color, and modify accordingly
        id = int(request.json["e_id"])
        entry = current_box.get_entry(id)
        color = request.json["color"]

        print(request.json)

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

    return ""

## Route Functions: Render main pages.

@app.route('/tester', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def tester():
    if request.method == "POST":
        if "submit" in request.form:
            print(current_box)
            # If is submit, next day and end.
            start_day()

    return render_template('tester.html', entries = current_box.get_current_cards())

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)