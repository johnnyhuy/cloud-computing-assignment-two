import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('Agg')
plt.style.use('seaborn')


class GraphBuilder:

    def __init__(self, state, council, suburb):
        self.locations = [state.name, council.name, suburb.name]
        self.crime_rates_per_100k = [
            state.per_100k_population_2019,
            council.per_100k_population_2019,
            suburb.get_2019_crime_rate_estimate(council)
        ]
        self.url = ""
        self.build_graph()

    def build_graph(self):
        image_name = '-'.join(self.locations).replace(' ', '_').lower()
        y_position = np.arange(len(self.locations))
        plt.bar(self.locations, self.crime_rates_per_100k, align='center', alpha=0.5)
        plt.xticks(y_position, self.locations)
        plt.ylabel('Crimes against a person per 100,0000 population', fontsize=10)
        plt.title('Crime')
        plt.plot()
        plt.show()
        self.url = 'static/images/generated/{0}.png'.format(image_name)
        plt.savefig(self.url)
        plt.close()

    def get_url(self):
        return self.url
