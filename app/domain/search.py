import json
import requests
import domain.constants as domain_constants


class Search:

    def __init__(self, domain_api_token,api_query):
        self.token = domain_api_token
        self.api_query = api_query

        # Appending to header constant to complete header variable
        domain_constants.SEARCH_PROPERTIES_HEADERS['Authorization'] = 'Bearer ' + self.token

        headers = domain_constants.SEARCH_PROPERTIES_HEADERS
        data = self.api_query

        try:
            response = requests.post(
                domain_constants.LISTINGS_SEARCH_URL,
                headers=headers,
                data=data
            )

            self.json_data = response.json()
        except Error as e:
            print(domain_constants.READ_API_ERROR, e)

    def get_data(self):
        return self.json_data
