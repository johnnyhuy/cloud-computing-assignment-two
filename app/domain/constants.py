# Auth credentials
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
LISTINGS_RESIDENTIAL_SEARCH_URL = 'https://api.domain.com.au/v1/listings/residential/_search'
LISTINGS_URL = 'https://api.domain.com.au/v1/listings/{0}'

SEARCH_PROPERTIES_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': ''
}

READ_API_ERROR = "Error reading data from API"
