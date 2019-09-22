DOMAIN_CLIENT_ID = 'client_9d78bbb90b7b4262b401ba918f41bbd7'
DOMAIN_SECRET = 'secret_5e495f5f90b176e7f391ff69cefa893c'
DOMAIN_TOKEN_GENERATOR_URL = 'https://auth.domain.com.au/v1/connect/token'
DOMAIN_TOKEN_GENERATOR_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
DOMAIN_TOKEN_GENERATOR_DATA = {
    'grant_type': 'client_credentials',
    'scope': 'api_addresslocators_read api_locations_read'
}
DOMAIN_LOCATION_PROFILE_URL_PREFIX = 'https://api.domain.com.au/v1/addressLocators?state=Vic&searchLevel=Suburb&suburb='