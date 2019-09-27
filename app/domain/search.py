import json
import requests
import domain.constants as domain_constants


class Search:

    def __init__(self, api_token):
        """
        Search class used to fetch data from the Domain API.

        :param api_token: API key from the Domain API
        """

        self.token = api_token
        self.headers = domain_constants.SEARCH_PROPERTIES_HEADERS
        domain_constants.SEARCH_PROPERTIES_HEADERS['Authorization'] = 'Bearer ' + self.token

    def get_residential(self, api_query):
        """
        Get residential data from the API

        :param api_query: JSON query to get content from the API
        """

        try:
            response = requests.post(
                domain_constants.LISTINGS_SEARCH_URL,
                headers=self.headers,
                data=json.dumps(api_query)
            )

            return response.json()
        except requests.exceptions.HTTPError as e:
            print(domain_constants.READ_API_ERROR, e)
