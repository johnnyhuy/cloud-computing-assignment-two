AUTH = ('client_9d78bbb90b7b4262b401ba918f41bbd7',
        'secret_5e495f5f90b176e7f391ff69cefa893c')
TOKEN_GENERATOR_URL = 'https://auth.domain.com.au/v1/connect/token'
DOMAIN_TOKEN_GENERATOR_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
TOKEN_GENERATOR_DATA = {
    'grant_type': 'client_credentials',
    'scope': 'api_addresslocators_read api_locations_read api_listings_read api_listings_read'
}

ADDRESS_LOCATORS_API_URL = 'https://api.domain.com.au/v1/addressLocators?state=Vic&searchLevel=Suburb&suburb='
LOCATION_PROFILES_API_URL = 'https://api.domain.com.au/v1/locations/profiles/'
LISTINGS_SEARCH_URL = 'https://api.domain.com.au/v1/listings/residential/_search'

SEARCH_PROPERTIES_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': ''
}

READ_API_ERROR = "Error reading data from API"

QUERY_DATA = '{' \
             '"listingType":"Sale",' \
             '"minBedrooms":MIN_BEDROOMS_PLACEHOLDER,' \
             '"maxBedrooms":MAX_BEDROOMS_PLACEHOLDER,' \
             '"minBathrooms":MIN_BATHROOMS_PLACEHOLDER,' \
             '"maxBathrooms":MAX_BATHROOMS_PLACEHOLDER,' \
             '"minCarspaces":MIN_CARSPACES_PLACEHOLDER,' \
             '"maxCarspaces":MAX_CARSPACES_PLACEHOLDER,' \
             '"locations":[{' \
             '"state":"VIC",' \
             '"suburb":"SUBURB_PLACEHOLDER"' \
             '}]}'
