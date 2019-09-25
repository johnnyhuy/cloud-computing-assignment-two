from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import ptvsd
import os
import json
from location import Suburb, Council, State
from data_grabber import SuburbData, CouncilData, StateData, FeesData, DomainAccessToken, SearchResponseData
from stats import GraphBuilder
import domain_api_constants

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if (os.getenv('ENVIRONMENT', 'production') == 'development'):
    ptvsd.enable_attach(address=('0.0.0.0', 8080))

global listings

domain_access_token = DomainAccessToken().get_token()

@app.get("/")
def index(request):
    # global listings
    return templates.TemplateResponse("index.html", {'request': request})

@app.post("/listing")
def index():
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

# @app.route("/listing/<property_id>", methods=['GET', 'POST'])
# def listing(property_id):
#     global listings

#     for p in listings:
#         if p['type'] == 'PropertyListing':
#             if str(p['listing']['id']) == property_id:

#                 suburb_data = SuburbData(p['listing']['propertyDetails']['suburb'], domain_access_token)
#                 suburb = Suburb(suburb_data.get_data())

#                 council_data = CouncilData(suburb.council_name)
#                 council = Council(council_data.get_data())

#                 state_data = StateData("Victoria")
#                 state = State(state_data.get_data())

#                 crime = None
#                 crime = GraphBuilder(state, council, suburb)
#                 crime_fig_url = crime.get_url()
#                 if request.method == 'POST':
#                     price_estimate = request.form.get('price_estimate')
#                     fees = FeesData(price_estimate)

#                     return render_template('listing.html', p=p, suburb=suburb, council=council, state=state,
#                                            crime_fig_url=crime_fig_url, fees=fees)
#                 else:
#                     return render_template('listing.html', p=p, suburb=suburb, council=council, state=state,
#                                            crime_fig_url=crime_fig_url)
#     return "Property Not Found"
