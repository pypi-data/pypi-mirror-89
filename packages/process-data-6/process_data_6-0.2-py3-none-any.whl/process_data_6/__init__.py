"""
DataProcessor inherits sklearn BaseEstimator and TransformerMixin to provide a data preprocessing pipeline which can be
used as a first step in a sklearn.pipeline in order to serialize data preprocessing and model in one pickle.

By now, data transformation are as follows and can be extended as needed

- Drop alternative_id, user_id, route_id and date features
- Get dummies
- Group several destination and origin type columns
- Shuffled data

"""

import pandas as pd
import numpy as np
import math


class GroupedDummies:  

    def __init__(self):
        pass
    
    @staticmethod
    def group_places_by_matcher(df_data, matcher, matcher_items):
        cols_origin_with_pt = [col for col in df_data.columns if 'pt_origin' in col]
        cols_destination_with_pt = [col for col in df_data.columns if 'pt_destination' in col]
        cols_origin_matching = [s for s in cols_origin_with_pt if any(xs in s for xs in matcher_items)]
        cols_destination_matching = [s for s in cols_destination_with_pt if any(xs in s for xs in matcher_items)]
        origin_matcher = 'pt_origin_' + matcher
        destination_matcher = 'pt_destination_' + matcher
        df_data[origin_matcher] = df_data[cols_origin_matching].sum(axis=1)
        df_data = df_data.drop(np.asarray(cols_origin_matching), axis=1)
        df_data[destination_matcher] = df_data[cols_destination_matching].sum(axis=1)
        df_data = df_data.drop(np.asarray(cols_destination_matching), axis=1)
        return df_data
    
    def process_data(self, df_data):
        df_data = df_data.drop(columns=['alternative_id', 'route_id', 'user_id', 'fecha'], axis=1)
        try:
            df_data = df_data.drop(columns=['_id', '_rev'])
        except KeyError:
            print()
            
        food_places_items = ['food', 'bar', 'cafe', 'night_club', 'restaurant']
        shopping_places_items = ['bicycle_store', 'book_store', 'clothing_store', 'convenience_store',
                                 'department_store',
                                 'electronics_store', 'furniture_store', 'hardware_store', 'home_goods_store',
                                 'jewelry_store',
                                 'liquor_store', 'pet_store', 'shoe_store', 'shopping_mall', 'supermarket']

        health_places_items = ['health', 'dentist', 'doctor', 'hospital', 'veterinary_care', 'physiotherapist']
        vehicle_related_places_items = ['gas_station', 'parking']
        df_data_grouped = self.group_places_by_matcher(df_data, 'food_places', food_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'shopping_places', shopping_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'health_places', health_places_items)
        df_data_grouped = self.group_places_by_matcher(df_data_grouped, 'vehicle_places', vehicle_related_places_items)
        columns_dummies = ['profileName']
        df_data_dummies = pd.get_dummies(df_data_grouped, columns=columns_dummies,drop_first=True)
        df_final = df_data_dummies 
        return df_final

    def fit(self, df_data, y=None):
        # Returns `self` unless something different happens in train and test
        return self
    
    def transform(self, df_data, y=None):
        # The workhorse of this feature extractor
        return self.process_data(df_data)
    

class Ordinal:

    def __init__(self):
        pass

    @staticmethod
    def ordinal_var(df_data):
        mapper_traffic = {'fluid': 0, 'medium': 1, 'heavy': 2}
        df_data.traffic = df_data.traffic.replace(mapper_traffic).astype(int)
        df_data.weather = df_data.weather.apply(lambda x: x.lower())
        mapper_weather = {'clear': 0,'mist': 1, 'clouds': 2, 'drizzle': 3,'rain':4 }
        df_data.weather = df_data.weather.replace(mapper_weather).astype(int)
        mapper_arrivaltimeslot = {'morning': 0, 'afternoon': 1, 'evening': 2, 'night': 3}
        df_data.arrivalTimeSlot = df_data.arrivalTimeSlot.replace(mapper_arrivaltimeslot).astype(int)
        mapper_departuretimeslot = {'morning': 0, 'afternoon': 1, 'evening': 2, 'night': 3}
        df_data.departureTimeSlot = df_data.departureTimeSlot.replace(mapper_departuretimeslot).astype(int)
        mapper_day_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                              'friday': 4, 'saturday': 5, 'sunday': 6}
        df_data.day_of_week = df_data.day_of_week.replace(mapper_day_of_week).astype(int)
        mapper_day_of_week_type = {'work': 0, 'weekend': 1}
        df_data.day_of_week_type = df_data.day_of_week_type.replace(mapper_day_of_week_type).astype(int)
        return df_data

    def fit(self, df_data, y=None):
        # Returns `self` unless something different happens in train and test
        return self

    def transform(self, df_data, y=None):
        # The workhorse of this feature extractor
        return self.ordinal_var(df_data)
    
    
class SelectedVars:  

    def __init__(self, var_used=None):
        self.var_used = var_used
    
    def drop_vars(self, df_data):
        df_data = df_data[list(self.var_used)]
        return df_data
    
    def fit(self, df_data, y=None):
        # Returns `self` unless something different happens in train and test
        return self
    
    def transform(self, df_data, y=None):
        # The workhorse of this feature extractor
        return self.drop_vars(df_data)
    

class Transform:  

    def __init__(self, var_num=None):
        self.var_num = var_num
    
    def transform_con(self, df_data):
        for column in self.var_num:
            if min(df_data[column]) > 0:
                df_data[column].apply(lambda x: math.log(x, 10))
        return df_data
    
    def fit(self, df_data, y=None):
        # Returns `self` unless something different happens in train and test
        return self
    
    def transform(self, df_data,  y=None):
        # The workhorse of this feature extractor
        return self.transform_con(df_data)