"""
Contains the house price controller.
"""
from house_price_model import construct_models
from house_price_model import get_base_date
import pandas as pd

# Constants
FOREST_FACTOR = 3.0
RIDGE_FACTOR = 0.001

# Construct the price models.
RIDGE_MODEL, FOREST_MODEL = construct_models()


def create_test_frame(incoming_feature_dictionary):
    """
    Creates a test data frame for a single home. To use, construct an incoming
    feature dictionary with the following keys:

    sale_year:      int (2014 or later)
    sale_month:     int (1 through 12; defaults to 1)
    sale_day:       int (1 through 28, 30 or 31; defaults to 1)
    bedrooms:       int (number of bedrooms)
    bathrooms:      float (number of bathrooms; may be factional)
    sqft_living:    int (square feet inside structure)
    sqft_lot:       int (square feet of property)
    floors:         int (number of floors)
    waterfront:     int (0 for No; 1 for Yes)
    view:           int (number of rooms with a view)
    condition:      int (1 through 5)
    grade:          int (1 through 15)
    sqft_above:     int (square feet of structure above ground)
    sqft_basement:  int (square feet of structure basement)
    yr_built:       int (year of construction)
    yr_renovated:   int (year of renovation; defaults to year built)
    zipcode:        int (ZIP Code of property address)
    latitude:       float (latitude of property)
    longitude:      float (longitude of property)
    sqft_living15:  int (unknown measure; defaults to sqft_living)
    sqft_lot15:     int (unknown measure; defaults to sqft_lot)
    list_price:     float (price at which the property was listed)

    :param incoming_feature_dictionary: A dictionary of house features
    :type incoming_feature_dictionary: dict
    :return: A data frame for the single described home
    """

    # Create a date-time object from the sales year, month and day.
    sales_date = pd.to_datetime(
        '{}{}{}'.format(incoming_feature_dictionary.get('sale_year'),
                        incoming_feature_dictionary.get('sale_month', 1),
                        incoming_feature_dictionary.get('sale_day', 1)),
        format='%Y%m%d', errors='ignore')

    # Create a dictionary with values describing the home.
    outgoing_feature_dictionary =\
        {'sale_day': (sales_date - get_base_date()).days + 1,
         'sale_day_of_week': pd.Categorical(sales_date.dayofweek),
         'sale_day_in_month': pd.Categorical(sales_date.day),
         'bedrooms': incoming_feature_dictionary.get('bedrooms'),
         'bathrooms': incoming_feature_dictionary.get('bathrooms'),
         'sqft_living': incoming_feature_dictionary.get('sqft_living'),
         'sqft_lot': incoming_feature_dictionary.get('sqft_lot'),
         'floors': pd.Categorical(incoming_feature_dictionary.get('floors')),
         'waterfront': pd.Categorical(
             incoming_feature_dictionary.get('waterfront')),
         'view': pd.Categorical(incoming_feature_dictionary.get('view')),
         'condition': pd.Categorical(
             incoming_feature_dictionary.get('condition')),
         'grade': pd.Categorical(incoming_feature_dictionary.get('grade')),
         'sqft_above': incoming_feature_dictionary.get('sqft_above'),
         'sqft_basement': incoming_feature_dictionary.get('sqft_basement'),
         'yr_built': pd.Categorical(
             incoming_feature_dictionary.get('yr_built')),
         'yr_renovated':
             pd.Categorical(incoming_feature_dictionary.get(
                 'yr_renovated',
                 incoming_feature_dictionary.get('yr_built'))),
         'zipcode': pd.Categorical(incoming_feature_dictionary.get('zipcode')),
         'lat': incoming_feature_dictionary.get('latitude'),
         'long': incoming_feature_dictionary.get('longitude'),
         'sqft_living15': incoming_feature_dictionary.get(
             'sqft_living15',
             incoming_feature_dictionary.get('sqft_living')),
         'sqft_lot15': incoming_feature_dictionary.get(
             'sqft_lot15',
             incoming_feature_dictionary.get('sqft_lot')),
         'list_price': incoming_feature_dictionary.get('list_price')
        }

    # Return a new data frame with the given data.
    return pd.DataFrame(data=outgoing_feature_dictionary, index=[0])


def predict_using_forest(house_frame):
    """
    Predicts a house price using the random forest model.

    :param house_frame: A data frame describing the house.
    :return: The predicted price of the house.
    """
    return round(float(FOREST_MODEL.predict(X=house_frame) * FOREST_FACTOR), 2)


def predict_using_ridge(house_frame):
    """
    Predicts a house price using the ridge regression model.

    :param house_frame: A data frame describing the house.
    :return: The predicted price of the house.
    """
    return round(float(RIDGE_MODEL.predict(X=house_frame) * RIDGE_FACTOR), 2)
