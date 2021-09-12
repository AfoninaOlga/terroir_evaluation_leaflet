from canton_repository import Canton, WeatherData
from db import query_db

elems = {"clay", "organic_matter", "silt", "sand", "phosphorus", "potassium", "calcium", "sodium", "pH", "limestone"}


class TerroirEvaluator:
    @staticmethod
    def get_amendment(factor):
        if (0.8 <= factor <= 1.1):
            return factor - 0.05
        elif (0.75 <= factor <= 0.79) or (0.15 <= factor <= 0.19):
            return factor - 0.04
        elif (0.66 <= factor <= 0.74) or (0.2 <= factor <= 0.24):
            return factor - 0.03
        elif 0.25 <= factor <= 0.65:
            return factor - 0.02
        else:
            return factor

    @staticmethod
    def get_additional_prop(organic_matter):
        factor = round(organic_matter * 10 / 2.1584, 2)
        if factor <= 55:
            return 0.7
        if factor <= 65:
            return 0.8
        if factor <= 75:
            return 0.85
        if factor <= 85:
            return 0.91
        if factor <= 95:
            return 0.96
        if factor <= 105:
            return 1
        if factor <= 115:
            return 1.05
        if factor <= 125:
            return 1.09
        if factor <= 135:
            return 1.12
        if factor <= 145:
            return 1.14
        return 1.15

    @staticmethod
    def get_ph_factor(pH):
        if pH < 4.5:
            return 0.87
        if pH <= 5:
            return 0.94
        if pH <= 5.5:
            return 1
        if pH <= 6:
            return 1.05
        return 1.1

    @staticmethod
    def get_potassium_factor(potassium):
        if potassium < 50:
            return 0.96
        if potassium <= 80:
            return 1
        return 1.04

    @staticmethod
    def get_phosphorus_factor(phosphorus):
        if phosphorus < 25:
            return 0.95
        if phosphorus < 90:
            return 1
        return 1.1

    @classmethod
    def eval_index(cls, canton: Canton, weather_data: WeatherData):
        t_diff = weather_data['t_max'] - weather_data['t_min']
        if not t_diff:
            t_diff = 10.3
        continental_factor = round(360 * (t_diff) / (canton['latitude'] + 10), 2)
        additional_prop = cls.get_additional_prop(canton['organic_matter'])
        agrochemical_indicator = cls.get_ph_factor(canton['pH']) * cls.get_phosphorus_factor(
            canton['phosphorus']) * cls.get_potassium_factor(canton['potassium'])
        moisture_factor = cls.get_amendment(weather_data['moisture_fact']) / 10
        index = round(12.5 * (2 - canton['density']) * canton['p'] * additional_prop * agrochemical_indicator
                     * weather_data['t_sum'] * moisture_factor / (continental_factor + 100), 2)

        return index

    @staticmethod
    def get_sutability(canton: Canton):
        optimality = dict()
        optimality['granulometric composition'] = 'optimum'
        optimality['total carbonates'] = 'optimum'

        organic_matter = canton['organic_matter'] / 10
        if organic_matter < 2.5:
            optimality['organic matter'] = 'minimum'
        elif organic_matter <= 3.5:
            optimality['organic matter'] = 'optimum'
        else:
            optimality['organic matter'] = 'maximum'

        bulk_density = canton['density']
        if bulk_density < 1.1:
            optimality['bulk density'] = 'minimum'
        elif bulk_density <= 1.35:
            optimality['bulk density'] = 'optimum'
        else:
            optimality['bulk density'] = 'maximum'

        pH = canton['pH']
        if pH < 6.5:
            optimality['pH'] = 'minimum'
        elif pH <= 8.5:
            optimality['pH'] = 'optimum'
        else:
            optimality['pH'] = 'maximum'

        sodium = canton['sodium'] / 10000
        if sodium < 3:
            optimality['exchangeable sodium'] = 'minimum'
        elif sodium <= 7:
            optimality['exchangeable sodium'] = 'optimum'
        else:
            optimality['exchangeable sodium'] = 'maximum'

        potassium = canton['potassium']
        if potassium < 30:
            optimality['potassium'] = 'very low'
        elif potassium <= 80:
            optimality['potassium'] = 'low'
        elif potassium <= 150:
            optimality['potassium'] = 'average'
        elif potassium <= 200:
            optimality['potassium'] = 'increased'
        elif potassium <= 300:
            optimality['potassium'] = 'high'
        else:
            optimality['potassium'] = 'very high'

        phosphorus = canton['phosphorus']
        if phosphorus < 60:
            optimality['phosphorus'] = 'very low'
        elif phosphorus <= 80:
            optimality['phosphorus'] = 'low'
        elif phosphorus <= 120:
            optimality['phosphorus'] = 'average'
        elif phosphorus <= 170:
            optimality['phosphorus'] = 'increased'
        elif phosphorus <= 250:
            optimality['phosphorus'] = 'high'
        else:
            optimality['phosphorus'] = 'very high'

        return optimality


def get_suitability(code):
    canton: Canton = query_db('SELECT * FROM Canton WHERE code = ?', [code])[0]
    return TerroirEvaluator.get_sutability(canton)