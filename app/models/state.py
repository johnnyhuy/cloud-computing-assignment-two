class State:

    def __init__(self, state_data_dict):
        self.name = state_data_dict['state_name']
        self.crimes_against_person_2019 = float(state_data_dict['crimes_against_person_2019'])
        self.per_100k_population_2019 = float(state_data_dict['per_100k_population_2019'])
        self.population_2019 = (100000 * self.crimes_against_person_2019) / self.per_100k_population_2019
