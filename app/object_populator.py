import mysql.connector
from mysql.connector import Error
import requests
from static import contants

class ObjectPopulator:
    crime_database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="password"
    )


    @staticmethod
    def populate_suburb_object(suburb):
        ObjectPopulator.__pull_sql_data(suburb)
        ObjectPopulator.__pull_json_data(suburb)

    def __pull_sql_data(suburb):
        """
        Queries database to collect info for:
            postcode,
            council_name,
            crimes_against_person_2016
            crimes_against_person_2019
        """
        try:
            # Connect to db
            mycursor = ObjectPopulator.crime_database.cursor(dictionary=True)

            mycursor.execute("SELECT * "
                             "FROM crime_data.suburbs "
                             "WHERE name = '" + suburb.name + "'"
                                                              ";")
            sub = mycursor.fetchall()[0]
            suburb.postcode = sub['postcode']
            suburb.council_name = sub['council_name']
            mycursor.execute("SELECT year_ending, sum(incidents_recorded) as total_incidents "
                             "FROM crime_data.crimes_vic_by_suburb "
                             "WHERE suburb_name = '" + suburb.name + "'"
                                                                     "AND offence_division_code = 'A'"
                                                                     "GROUP BY year_ending "
                                                                     ";")
            sub_crimes_by_year = mycursor.fetchall()
            for crime in sub_crimes_by_year:
                if (crime['year_ending'] == 2016):
                    suburb.crimes_against_person_2016 = crime['total_incidents']
                if (crime['year_ending'] == 2019):
                    suburb.crimes_against_person_2019 = crime['total_incidents']

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (ObjectPopulator.crime_database.is_connected()):
                ObjectPopulator.crime_database.close()
                mycursor.close()
                print("MySQL connection is closed")

    def __pull_json_data(suburb):
        """
        Gets population from Domain API
        """
        try :
            access_token_response = requests.post(contants.DOMAIN_TOKEN_GENERATOR_URL,
                                     headers=contants.DOMAIN_TOKEN_GENERATOR_HEADERS,
                                     data=contants.DOMAIN_TOKEN_GENERATOR_DATA,
                                     auth=(contants.DOMAIN_CLIENT_ID, contants.DOMAIN_SECRET))

            access_token = access_token_response.json()['access_token']

            headers = {'accept': 'application/json',
                        'Authorization': 'Bearer ' + access_token
                        }
            suburb_id_response = requests.get(contants.DOMAIN_LOCATION_PROFILE_URL_PREFIX + suburb.name, headers=headers)
            domain_suburb_id = suburb_id_response.json()[0]['ids'][0]['id']

            response = requests.get('https://api.domain.com.au/v1/locations/profiles/' + str(domain_suburb_id), headers=headers)
            suburb.population_in_2016 = response.json()['data']['population']
        except Error as e:
            print("Error reading data from API", e)