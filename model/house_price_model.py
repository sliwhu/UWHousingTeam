"""
Contains the house price model.

DON'T USE THIS MODEL!  Use the HousePriceModel in house_price_model_2.py.
"""
import numpy as np
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import RidgeCV

# Constants
BASE_DATE = pd.to_datetime('20140101', format='%Y%m%d', errors='ignore')
TO_TYPE = 'category'

# Note: It is expected that the following environment variables will be set so
# that the house price model will be able to locate its training data:
#
# SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
# SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"
#
# os.environ["SALES_DATA_PATH"] = '~/UW Data Science/DATA 515A/Project'
# os.environ["SALES_DATA_FILE"] = 'Merged_Data_excel.csv'  # 'KingCountyHomeSalesData.csv'

# Construct the sales data path, and read the sales data.
SALES_DATA_PATH = os.path.join(os.environ['SALES_DATA_PATH'], os.environ['SALES_DATA_FILE'])
SALES_DATA = pd.read_csv(SALES_DATA_PATH, parse_dates=['date'])


# Data cleansing plan:
#
# id:               Discard
# date:             Convert to integer; make categorical
# price:            No conversion
# bedrooms:         No conversion
# bathrooms:        No conversion
# sqft_living:      No conversion
# sqft_lot:         No conversion
# floors:           Make categorical
# waterfront:       Make categorical
# view:             Make categorical
# condition:        Make categorical
# grade:            Make categorical
# sqft_above:       No conversion
# sqft_basement:    No conversion
# yr_built:         Make categorical
# yr_renovated:     Copy over yr_built if missing; make categorical
# zipcode:          Make categorical
# lat:              No conversion
# long:             No conversion
# sqft_living15     No conversion
# sqft_lot15        No conversion
# list_price        No conversion


def construct_models():
    """
    Constructs a ridge regression model, and a random forest model for housing
    price data.

    :return: A ridge regression model, and a random forest model for housing
    price data
    """
    return train_models(create_model_data_frame(SALES_DATA))


def create_model_data_frame(source):
    """
    Creates a data frame suitable for constructing a model.

    :param source: The source data frame
    :return: A data frame suitable for constructing a model
    """

    # Create an empty data frame.  Get the date series from the source.
    my_model_data = pd.DataFrame()
    sales_date = source['date']

    # Extract the sales date as an integer.
    my_model_data['sale_day'] =\
        (sales_date - get_base_date()).astype('timedelta64[D]').astype(int) + 1

    # Extract the sale day-of-week as an integer, and the sale day in month.
    my_model_data['sale_day_of_week'] = sales_date.dt.dayofweek.astype(TO_TYPE)
    my_model_data['sale_day_in_month'] = sales_date.dt.day.astype(TO_TYPE)

    # Extract common features as numeric, or categorical values.
    # create_model_feature(my_model_data, source, 'price', False)
    create_model_feature(my_model_data, source, 'price', False)
    create_model_feature(my_model_data, source, 'bedrooms', False)
    create_model_feature(my_model_data, source, 'bathrooms', False)
    create_model_feature(my_model_data, source, 'sqft_living', False)
    create_model_feature(my_model_data, source, 'sqft_lot', False)
    create_model_feature(my_model_data, source, 'floors', True)
    create_model_feature(my_model_data, source, 'waterfront', True)
    create_model_feature(my_model_data, source, 'view', True)
    create_model_feature(my_model_data, source, 'condition', True)
    create_model_feature(my_model_data, source, 'grade', True)
    create_model_feature(my_model_data, source, 'sqft_above', False)
    create_model_feature(my_model_data, source, 'sqft_basement', False)
    create_model_feature(my_model_data, source, 'yr_built', True)

    # Use 'year built' in place of 'year renovated' if year renovated is zero
    # in the source.
    field_name = 'yr_renovated'
    my_model_data[field_name] = pd.Categorical(np.where(
        source[field_name] == 0,
        source['yr_built'].astype(TO_TYPE),
        source[field_name].astype(TO_TYPE)))

    # Extract more common features as numeric, or categorical values.
    create_model_feature(my_model_data, source, 'zipcode', True)
    create_model_feature(my_model_data, source, 'lat', False)
    create_model_feature(my_model_data, source, 'long', False)
    create_model_feature(my_model_data, source, 'sqft_living15', False)
    create_model_feature(my_model_data, source, 'sqft_lot15', False)
    my_model_data['list_price'] = source['List price']

    # Return the completed model data frame.
    return my_model_data


def create_model_feature(destination, source, name, to_categorical=False):
    """
    Creates a feature in a destination data frame.

    :param destination: The destination data frame
    :param source: The source data frame
    :param name: The name of the feature to copy
    :param to_categorical: True if the feature should be converted to
    categorical, false otherwise
    :return: None
    """
    if to_categorical:
        destination[name] = source[name].astype(TO_TYPE)
    else:
        destination[name] = source[name]
    return None


def get_base_date():
    """
    Gets the base date as a reference for day of sale.

    :return: The base date as a reference for day of sale
    """
    return BASE_DATE


def train_models(my_model_data):
    """
    Trains a ridge regression model, and a random forest model, and returns
    them.

    :param my_model_data: The model data on which to train
    :return: A ridge regression model, and a random forest model
    """

    # Construct the ridge regression model.
    my_ridge_model = RidgeCV(alphas=(0.1, 1.0, 10.0),
                             fit_intercept=True,
                             normalize=True,
                             scoring=None,
                             cv=None,
                             gcv_mode=None,
                             store_cv_values=True)

    # Construct the random forest model.
    my_forest_model = RandomForestRegressor()

    # Divide the model data into predictor and response.
    response_field = 'price'
    predictors = my_model_data.ix[:, response_field != my_model_data.columns]
    response = my_model_data[response_field]

    # Fit the models, and return them.
    my_ridge_model.fit(X=predictors, y=response)
    my_forest_model.fit(X=predictors, y=response)
    return my_ridge_model, my_forest_model
