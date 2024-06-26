import mysql.connector
from mysql.connector import Error
import os
import requests
import domain.constants as domain_constants
import domain.fee_constants as fee_constants


class DomainAccessToken:

    def __init__(self):
        try:
            access_token_response = requests.post(
                domain_constants.TOKEN_GENERATOR_URL,
                headers=domain_constants.DOMAIN_TOKEN_GENERATOR_HEADERS,
                data=domain_constants.TOKEN_GENERATOR_DATA,
                auth=(
                    os.getenv('DOMAIN_API_AUTH_CLIENT'),
                    os.getenv('DOMAIN_API_AUTH_SECRET')
                )
            )

            self.token = access_token_response.json()['access_token']
        except Error as e:
            print(domain_constants.READ_API_ERROR, e)

    def get_token(self):
        return self.token


class SuburbData:

    def __init__(self, suburb_name, domain_api_token):
        self.data_dict = {'suburb_name': suburb_name}
        self.__pull_sql_data()
        self.__pull_json_data(domain_api_token)

    def __pull_sql_data(self):

        crime_database = mysql.connector.connect(
            host=os.getenv('STAYAPP_DATABASE_HOST'),
            user=os.getenv('STAYAPP_DATABASE_USER'),
            passwd=os.getenv('STAYAPP_DATABASE_PASSWORD')
        )

        """
        Queries database to collect info for:
            postcode,
            council_name,
            crimes_against_person_2016
            crimes_against_person_2019
        """
        cursor = crime_database.cursor(dictionary=True)

        try:

            cursor.execute("SELECT * "
                           "FROM stayapp.suburbs "
                           "WHERE name = '" + self.data_dict['suburb_name'] + "'"
                                                                              ";")
            sub = cursor.fetchall()[0]
            self.data_dict['postcode'] = sub['postcode']
            self.data_dict['council_name'] = sub['council_name']
            cursor.execute("SELECT year_ending, sum(incidents_recorded) as total_incidents "
                           "FROM stayapp.crimes_vic_by_suburb "
                           "WHERE suburb_name = '" + self.data_dict['suburb_name'] + "'"
                                                                                     "AND offence_division_code = 'A'"
                                                                                     "GROUP BY year_ending "
                                                                                     ";")
            sub_crimes_by_year = cursor.fetchall()
            for crime in sub_crimes_by_year:
                if crime['year_ending'] == 2016:
                    self.data_dict['crimes_against_person_2016'] = crime['total_incidents']
                if crime['year_ending'] == 2019:
                    self.data_dict['crimes_against_person_2019'] = crime['total_incidents']

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if crime_database.is_connected():
                crime_database.close()
                cursor.close()
                print("MySQL connection is closed")

    def __pull_json_data(self, domain_api_token):

        try:
            # Get location ID
            address_locators_url = domain_constants.ADDRESS_LOCATORS_API_URL + self.data_dict['suburb_name']

            headers = {
                'accept': 'application/json',
                'Authorization': 'Bearer ' + domain_api_token
            }

            locations_profile_response = requests.get(
                address_locators_url,
                headers=headers)

            domain_suburb_id = locations_profile_response.json()[0]['ids'][0]['id']

            # Get population data
            location_profile_url = domain_constants.LOCATION_PROFILES_API_URL + str(domain_suburb_id)

            locators_response = requests.get(
                location_profile_url,
                headers=headers
            )
            self.data_dict['population_in_2016'] = locators_response.json()['data']['population']
        except Error as e:
            print(domain_constants.READ_API_ERROR, e)

    def get_data(self):
        return self.data_dict


class CouncilData:

    def __init__(self, council_name):
        self.data_dict = {'council_name': council_name}
        self.__pull_sql_data()

    def __pull_sql_data(self):
        crime_database = mysql.connector.connect(
            host=os.getenv('STAYAPP_DATABASE_HOST'),
            user=os.getenv('STAYAPP_DATABASE_USER'),
            passwd=os.getenv('STAYAPP_DATABASE_PASSWORD')
        )

        """
        Queries database to collect info for:
            land_area
            population_2016
            crimes_against_person_2016,
            crimes_against_person_2019,
            per_100k_population_2016 (also for crimes against a person)
            per_100k_population_2019 (also for crimes against a person)
        """
        cursor = crime_database.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * "
                           "FROM "
                           "stayapp.councils "
                           "WHERE name = '" + self.data_dict['council_name'] + "'"
                                                                               ";")
            cn = cursor.fetchall()[0]
            self.data_dict['land_area'] = cn['land_area']
            self.data_dict['population_2016'] = cn['population_2016']

            cursor.execute("SELECT year_ending, sum(incidents_recorded) as total_incidents "
                           "FROM stayapp.crimes_vic_by_council "
                           "WHERE council_name = '" + self.data_dict['council_name'] + "'"
                                                                                       "AND offence_division_code = 'A'"  # A = crimes against a person
                                                                                       "GROUP BY year_ending "
                                                                                       ";")
            council_crimes_by_year = cursor.fetchall()
            for crime in council_crimes_by_year:
                if crime['year_ending'] == 2016:
                    self.data_dict['crimes_against_person_2016'] = crime['total_incidents']
                if crime['year_ending'] == 2019:
                    self.data_dict['crimes_against_person_2019'] = crime['total_incidents']

            cursor.execute("SELECT year_ending, sum(lga_rate_per_100000_population) as total_rate "
                           "FROM stayapp.crimes_vic_by_council "
                           "WHERE council_name = '" + self.data_dict['council_name'] + "'"
                                                                                       "AND offence_division_code = 'A'"  # A = crimes against a person
                                                                                       "GROUP BY year_ending "
                                                                                       ";")
            council_crimes_by_year = cursor.fetchall()
            for crime in council_crimes_by_year:
                if crime['year_ending'] == 2016:
                    self.data_dict['per_100k_population_2016'] = crime['total_rate']
                if crime['year_ending'] == 2019:
                    self.data_dict['per_100k_population_2019'] = crime['total_rate']

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if crime_database.is_connected():
                crime_database.close()
                cursor.close()
                print("MySQL connection is closed")

    def get_data(self):
        return self.data_dict


class StateData:

    def __init__(self, state_name):
        self.data_dict = {'state_name': state_name}
        self.__pull_sql_data()

    def __pull_sql_data(self):
        crime_database = mysql.connector.connect(
            host=os.getenv('STAYAPP_DATABASE_HOST'),
            user=os.getenv('STAYAPP_DATABASE_USER'),
            passwd=os.getenv('STAYAPP_DATABASE_PASSWORD')
        )

        """
        Queries database to collect info for:
            crimes_against_person_2019,
            per_100k_population_2019 (also for crimes against a person)
        """
        cursor = crime_database.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT year_ending, offence_division_code,sum(incidents_recorded) total_incidents, "
                "sum(rate_per_100000_population) rate "
                "FROM stayapp.crimes_vic "
                "WHERE offence_division_code = 'A' "
                "AND year_ending = '2019' "
                "GROUP BY year_ending, offence_division_code")

            state = cursor.fetchall()[0]
            self.data_dict['crimes_against_person_2019'] = state['total_incidents']
            self.data_dict['per_100k_population_2019'] = state['rate']

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if crime_database.is_connected():
                crime_database.close()
                cursor.close()
                print("MySQL connection is closed")

    def get_data(self):
        return self.data_dict


class FeesData:

    def __init__(self, price_estimate):
        self.price_estimate = float(price_estimate)
        self.rate = 0
        self.base_cost = 0
        self.calculated_above = 0
        self.__pull_sql_data()

        self.stamp_duty = self.base_cost + (self.price_estimate - self.calculated_above) * self.rate
        self.mortgage_registration_fee = fee_constants.MORTGAGE_REGISTRATION_FEE
        self.land_transfer_fee = fee_constants.LAND_TRANSFER_RATE * int((self.price_estimate / 1000))
        self.conveyancing_fee = fee_constants.CONVEYANCING_FEE
        self.total_fees = self.stamp_duty + self.land_transfer_fee + self.mortgage_registration_fee + self.conveyancing_fee

    def __pull_sql_data(self):
        crime_database = mysql.connector.connect(
            host=os.getenv('STAYAPP_DATABASE_HOST'),
            user=os.getenv('STAYAPP_DATABASE_USER'),
            passwd=os.getenv('STAYAPP_DATABASE_PASSWORD')
        )

        cursor = crime_database.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM stayapp.stamp_duty_2019 WHERE " + str(
                self.price_estimate) + " > min_threshold ORDER BY min_threshold DESC LIMIT 1;")

            fees = cursor.fetchall()[0]

            self.rate = float(fees['rate'])
            self.base_cost = float(fees['base_cost'])
            self.calculated_above = float(fees['calculated_above'])

        except Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if crime_database.is_connected():
                crime_database.close()
                cursor.close()
                print("MySQL connection is closed")
