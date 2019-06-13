from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        request_dict = request.form.to_dict()
        # Get the key value of the id, both values are strings
        color = list(request_dict)[0]
        id = int(request_dict[color])

        print(id, color)

    # Create the homepage; basic tester
    # Mock Data
    d1 = dict(
        id=0,
        priority=1,
        color='blue',
        text='1 - Test Message One'
    )

    d2 = dict(
        id=1,
        priority=2,
        color='blue',
        text='2 - Test Message Two'
    )

    d3 = dict(
        id=2,
        priority=3,
        color='blue',
        text='3 - Test Message Three'
    )

    # For now, we store them in a list and iterate through them all
    # We generate an example list for text, as we develop text first
    entries = [d3, d2, d1]

    # Sort entires by priority before rendering
    entries.sort(key=lambda x: x["priority"])

    return render_template('tester.html', entries = entries)


if __name__ == '__main__':
    app.run()
