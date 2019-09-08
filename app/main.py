from flask import Flask, render_template
import json
from app.suburb import Suburb
from app.object_populator import ObjectPopulator

app = Flask(__name__)

with open('./static/response_1567049463301.json') as json_file:
    listings = json.load(json_file)

@app.route("/")
def index():
    return render_template('index.html', listings=listings)


@app.route("/listing/<property_id>")
def listing(property_id):
    for p in listings:
        if str(p['listing']['id']) == property_id:
            suburb = Suburb(['propertyDetails']['suburb'])
            ObjectPopulator.populate_suburb_object(suburb)
            return render_template('listing.html', p=p,suburb=suburb)
    return "Property Not Found"


if __name__ == "__main__":
    app.run()
