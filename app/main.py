from fastapi import FastAPI, Form
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import ptvsd
import os
import json
from location import Suburb, Council, State
from domain.search import Search
from data_grabber import SuburbData, CouncilData, StateData, FeesData, DomainAccessToken, SearchResponseData
from stats import GraphBuilder
import domain_api_constants
from pydantic import BaseModel


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

if (os.getenv('ENVIRONMENT', 'production') == 'development'):
    ptvsd.enable_attach(address=('0.0.0.0', 8080))

domain_access_token = DomainAccessToken().get_token()

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/listings/')
def index(
    request: Request,
    suburb_name: str = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    carspaces: int = Form(...)
):
    listing = {
        'listingType': 'Sale',
        'locations': [
            {
                'state': 'VIC',
                'suburb': suburb_name
            }
        ],
        'maxBedrooms': bedrooms,
        'maxBathrooms': bathrooms,
        'maxCarspaces': carspaces
    }
    listing_query_json = json.dumps(listing)
    listings = Search(domain_access_token, listing_query_json).get_data()

    # Local only
    # listings = {}
    # with open('static/test_property_result.json', 'r') as outfile:
    #     listings = json.load(outfile)

    return templates.TemplateResponse(
        'listings.html',
        {
            'request': request,
            'listings': listings
        }
    )

@app.get('/listing/{property_id}')
def listing(property_id: int):

    # for listing in listings:
    #     if str(listing['listing']['id']) == property_id:
    #         suburb_data = SuburbData(listing['listing']['propertyDetails']['suburb'], domain_access_token)
    #         suburb = Suburb(suburb_data.get_data())

    #         council_data = CouncilData(suburb.council_name)
    #         council = Council(council_data.get_data())

    #         state_data = StateData('Victoria')
    #         state = State(state_data.get_data())

    #         crime = None
    #         crime = GraphBuilder(state, council, suburb)
    #         crime_fig_url = crime.get_url()

    #         if request.method == 'POST':
    #             price_estimate = request.form.get('price_estimate')
    #             fees = FeesData(price_estimate)

    #             return render_template('listing.html', listing=listing, suburb=suburb, council=council, state=state,
    #                                     crime_fig_url=crime_fig_url, fees=fees)
    #         else:
    #             return render_template('listing.html', listing=listing, suburb=suburb, council=council, state=state,
    #                                     crime_fig_url=crime_fig_url)

    return "Property Not Found"
