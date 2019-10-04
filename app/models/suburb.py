class Suburb:

    def __init__(self, suburb_data_dict):
        self.name = suburb_data_dict['suburb_name'].title()
        self.postcode = suburb_data_dict['postcode']
        self.council_name = suburb_data_dict['council_name']
        self.crimes_against_person_2016 = float(suburb_data_dict['crimes_against_person_2016'])
        self.crimes_against_person_2019 = float(suburb_data_dict['crimes_against_person_2019'])
        self.population_in_2016 = float(suburb_data_dict['population_in_2016'])
        self.per_100k_population_2016 = self.crimes_against_person_2016 / self.population_in_2016

    def get_2019_population_estimate(self, council):
        return (council.population_2019 / council.population_2016) * self.population_in_2016

    def get_2019_crime_rate_estimate(self, council):
        return (self.crimes_against_person_2019 / self.get_2019_population_estimate(council)) * 100000

    def get_low_high_crime_state_2019(self, council):
        if self.get_2019_crime_rate_estimate(council) < council.per_100k_population_2019:
            return 'lower'
        else:
            return 'higher'
