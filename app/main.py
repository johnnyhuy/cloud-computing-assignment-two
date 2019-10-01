from fastapi import FastAPI, Form, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
# import pydevd_pycharm
import os
import ptvsd
from location import Suburb, Council, State
from domain.search import Search
from data_grabber import SuburbData, CouncilData, StateData, FeesData, DomainAccessToken
from stats import GraphBuilder

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

if os.getenv('ENVIRONMENT', 'production') == 'development':
    ptvsd.enable_attach()
    # pydevd_pycharm.settrace('host.docker.internal', port=8081)


domain_access_token = DomainAccessToken().get_token()
search = Search(domain_access_token)


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
    listings = search.get_residential_listings(listing)

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
def listing(request: Request, property_id: int):
    listing = search.get_residential_listing(property_id)

    if (listing.get('message') == 'Not Found'):
        raise HTTPException(status_code=404, detail="Property not found")

    suburb_name = listing.get('addressParts').get('suburb')
    suburb_data = SuburbData(suburb_name, domain_access_token)
    suburb = Suburb(suburb_data.get_data())

    council_data = CouncilData(suburb.council_name)
    council = Council(council_data.get_data())

    state_data = StateData('Victoria')
    state = State(state_data.get_data())

    crime = None
    crime = GraphBuilder(state, council, suburb)
    crime_fig_url = crime.get_url()

    if request.method == 'POST':
        price_estimate = request.form.get('price_estimate')
        fees = FeesData(price_estimate)

        return render_template('listing.html', listing=listing, suburb=suburb, council=council, state=state,
                               crime_fig_url=crime_fig_url, fees=fees)
    else:
        return templates.TemplateResponse(
            'listing.html',
            {
                'request': request,
                'listing': listing,
                'suburb': suburb,
                'council': council,
                'state': state,
                'crime_fig_url': crime_fig_url
            }
        )
