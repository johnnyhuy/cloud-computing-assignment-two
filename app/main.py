from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/")
def index():
    with open('./static/response_1567049463301.json') as json_file:
        listings = json.load(json_file)
    return render_template('index.html',listings=listings)


@app.route("/property")
def property():
    return render_template('property.html')


if __name__ == "__main__":
    app.run()
