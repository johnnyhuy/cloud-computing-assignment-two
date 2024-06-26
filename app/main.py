from fastapi import FastAPI, Form, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from models.council import Council
from models.suburb import Suburb
from models.state import State
from domain.search import Search
from data_grabber import SuburbData, CouncilData, StateData, FeesData, DomainAccessToken
from stats.graph_builder import GraphBuilder
import os
import ptvsd
# import pydevd_pycharm

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

if os.getenv('ENVIRONMENT', 'production') == 'development':
    ptvsd.enable_attach()
    # pydevd_pycharm.settrace('host.docker.internal', port=8081)


domain_access_token = DomainAccessToken().get_token()
search = Search(domain_access_token)


@app.get('/', name='home')
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/listings/', name='get_listings')
def index(
    request: Request,
    suburb_name: str = Form(...),
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    carspaces: int = Form(...),
    honey: str = Form(None)
):
    if honey:
        return RedirectResponse(url='/', status_code=303)

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
    listings = search.get_residential_listings(listing)

    # Local only
    # listings = {}
    # with open('static/test_property_result.json', 'r') as outfile:
    #     listings = json.load(outfile)

    return templates.TemplateResponse(
        'listings/index.html',
        {
            'request': request,
            'listings': listings
        }
    )


@app.get('/listing/{property_id}', name='get_listing')
def listing(request: Request, property_id: int):
    listing = search.get_residential_listing(property_id)

    if listing.get('message') == 'Not Found':
        raise HTTPException(status_code=404, detail="Property not found")

    suburb_name = listing.get('addressParts').get('suburb')
    suburb_data = SuburbData(suburb_name, domain_access_token)
    suburb = Suburb(suburb_data.get_data())

    council_data = CouncilData(suburb.council_name)
    council = Council(council_data.get_data())

    state_data = StateData('Victoria')
    state = State(state_data.get_data())

    crime = GraphBuilder(state, council, suburb)
    crime_fig_url = crime.get_url()

    return templates.TemplateResponse(
        'listings/show.html',
        {
            'request': request,
            'listing': listing,
            'suburb': suburb,
            'council': council,
            'state': state,
            'crime_fig_url': crime_fig_url
        }
    )


@app.post('/listing/{property_id}/price', name='get_price')
def listing(
    request: Request,
    property_id: int,
    price_estimate: str = Form(...)
):
    listing = search.get_residential_listing(property_id)

    if listing.get('message') == 'Not Found':
        raise HTTPException(status_code=404, detail="Property not found")

    suburb_name = listing.get('addressParts').get('suburb')
    suburb_data = SuburbData(suburb_name, domain_access_token)
    suburb = Suburb(suburb_data.get_data())

    council_data = CouncilData(suburb.council_name)
    council = Council(council_data.get_data())

    state_data = StateData('Victoria')
    state = State(state_data.get_data())

    crime = GraphBuilder(state, council, suburb)
    crime_fig_url = crime.get_url()

    fees = FeesData(price_estimate)

    return templates.TemplateResponse(
        'listings/show.html',
        {
            'request': request,
            'listing': listing,
            'suburb': suburb,
            'council': council,
            'state': state,
            'crime_fig_url': crime_fig_url,
            'fees': fees
        }
    )
