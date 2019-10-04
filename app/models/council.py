class Council:
    def __init__(self, council_data_dict):
        self.name = council_data_dict['council_name']
        self.land_area = float(council_data_dict['land_area'])
        self.crimes_against_person_2016 = float(council_data_dict['crimes_against_person_2016'])
        self.crimes_against_person_2019 = float(council_data_dict['crimes_against_person_2019'])
        self.per_100k_population_2016 = float(council_data_dict['per_100k_population_2016'])
        self.per_100k_population_2019 = float(council_data_dict['per_100k_population_2019'])
        self.population_2016 = (100000 * self.crimes_against_person_2016) / self.per_100k_population_2016
        self.population_2019 = (100000 * self.crimes_against_person_2019) / self.per_100k_population_2019

    def get_low_high_crime_state_2019(self, state):
        if self.per_100k_population_2019 < state.per_100k_population_2019:
            return 'lower'
        else:
            return 'higher'
