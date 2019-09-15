from flask import Flask, render_template, request
import json

from location import Suburb, Council, State
from data_grabber import SuburbData, CouncilData, StateData, FeesData, DomainAccessToken, SearchResponseData
from stats import GraphBuilder
import domain_api_constants

app = Flask(__name__)

global listings

domain_access_token = DomainAccessToken().get_token()

@app.route("/", methods=['GET', 'POST'])
def index():
    global listings
    if request.method == 'POST':

        api_query = domain_api_constants.QUERY_DATA \
            .replace('SUBURB_PLACEHOLDER', request.form.get('suburb_name')) \
            .replace('MIN_BEDROOMS_PLACEHOLDER', str(request.form.get('min_bedrooms'))) \
            .replace('MAX_BEDROOMS_PLACEHOLDER', str(request.form.get('max_bedrooms')) )\
            .replace('MIN_BATHROOMS_PLACEHOLDER', str(request.form.get('min_bathrooms'))) \
            .replace('MAX_BATHROOMS_PLACEHOLDER', str(request.form.get('max_bathrooms'))) \
            .replace('MIN_CARSPACES_PLACEHOLDER', str(request.form.get('min_carspaces'))) \
            .replace('MAX_CARSPACES_PLACEHOLDER', str(request.form.get('max_carspaces')))
        listings = SearchResponseData(domain_access_token, api_query).get_data()
        return render_template('index.html', listings=listings)
    else:
        return render_template('index.html')


@app.route("/listing/<property_id>", methods=['GET', 'POST'])
def listing(property_id):
    global listings

    for p in listings:
        if p['type'] == 'PropertyListing':
            if str(p['listing']['id']) == property_id:

                suburb_data = SuburbData(p['listing']['propertyDetails']['suburb'], domain_access_token)
                suburb = Suburb(suburb_data.get_data())

                council_data = CouncilData(suburb.council_name)
                council = Council(council_data.get_data())

                state_data = StateData("Victoria")
                state = State(state_data.get_data())

                crime = GraphBuilder(state, council, suburb)
                crime_fig_url = crime.get_url()
                if request.method == 'POST':
                    price_estimate = request.form.get('price_estimate')
                    fees = FeesData(price_estimate)

                    return render_template('listing.html', p=p, suburb=suburb, council=council, state=state,
                                           crime_fig_url=crime_fig_url, fees=fees)
                else:
                    return render_template('listing.html', p=p, suburb=suburb, council=council, state=state,
                                           crime_fig_url=crime_fig_url)
    return "Property Not Found"


if __name__ == "__main__":
    app.run()
