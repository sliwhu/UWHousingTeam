"""
Contains a house price model for King County, Washington.
"""
import datetime as dt
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler


class HousePriceModel(object):
    """
    Contains a house price model for King County, Washington.
    """

    def __init__(self):
        """
        Initializes the house price model.
        """

        # Note: It is expected that the following environment variables will be
        # set so that the house price model will be able to locate its training
        # data:
        #
        # SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
        # SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"
        #
        # Comment out the following lines if these values are known to be set.
        #
        os.environ["SALES_DATA_PATH"] = '~/UW Data Science/DATA 515A/Project'
        os.environ["SALES_DATA_FILE"] = 'Merged_Data_excel.csv'  # 'KingCountyHomeSalesData.csv'

        # Declare and initialize the base date, and the scaler.
        self.base_date = HousePriceModel.create_date(2014, 1, 1)
        self.scaler = StandardScaler()

        # Declare and initialize the zip code dictionary.
        self.zipcode_dict = {'98002': (0, 234284.0),
                             '98168': (1, 240328.4),
                             '98032': (2, 251296.2),
                             '98001': (3, 280804.7),
                             '98148': (4, 284908.6),
                             '98023': (5, 286742.8),
                             '98188': (6, 289078.3),
                             '98003': (7, 294111.3),
                             '98030': (8, 296188.0),
                             '98031': (9, 300539.9),
                             '98198': (10, 302896.7),
                             '98055': (11, 304262.1),
                             '98178': (12, 310612.8),
                             '98042': (13, 311632.1),
                             '98022': (14, 315709.3),
                             '98106': (15, 319581.4),
                             '98092': (16, 334921.1),
                             '98058': (17, 353619.1),
                             '98108': (18, 355678.5),
                             '98146': (19, 359496.3),
                             '98038': (20, 366876.1),
                             '98133': (21, 386997.4),
                             '98118': (22, 417645.3),
                             '98056': (23, 420895.5),
                             '98155': (24, 423736.9),
                             '98126': (25, 424734.6),
                             '98019': (26, 424815.1),
                             '98014': (27, 455617.1),
                             '98028': (28, 462488.9),
                             '98166': (29, 464322.4),
                             '98125': (30, 469485.0),
                             '98070': (31, 487480.5),
                             '98011': (32, 490377.1),
                             '98059': (33, 493625.3),
                             '98034': (34, 521740.0),
                             '98065': (35, 528003.1),
                             '98136': (36, 551768.5),
                             '98072': (37, 570073.5),
                             '98117': (38, 576834.8),
                             '98107': (39, 579109.8),
                             '98103': (40, 585048.8),
                             '98144': (41, 594706.5),
                             '98029': (42, 612642.7),
                             '98027': (43, 617054.0),
                             '98007': (44, 617254.0),
                             '98116': (45, 618695.1),
                             '98115': (46, 619944.1),
                             '98122': (47, 634558.1),
                             '98052': (48, 645244.2),
                             '98008': (49, 645628.2),
                             '98177': (50, 676419.4),
                             '98053': (51, 678275.7),
                             '98077': (52, 682886.0),
                             '98074': (53, 685675.8),
                             '98075': (54, 790734.7),
                             '98199': (55, 792187.9),
                             '98033': (56, 803990.8),
                             '98005': (57, 810289.7),
                             '98119': (58, 849714.8),
                             '98006': (59, 859938.6),
                             '98105': (60, 863228.9),
                             '98109': (61, 880077.8),
                             '98102': (62, 901516.2),
                             '98112': (63, 1096239.0),
                             '98040': (64, 1194873.6),
                             '98004': (65, 1356524.0)
                            }

        # Declare and initialize member variables that will be set during
        # intialize_model().
        self.mean_response = 0
        self.model = RidgeCV()
        self.predictors = pd.DataFrame()
        self.sales_data = pd.DataFrame()
        return None

    def calculate_sale_day_by_date(self, date):
        """
        Calculates sales days for a date series.
        :param date: A date series
        :return: A series of sales days
        """
        return (date - self.get_base_date())\
                   .astype('timedelta64[D]').astype(int) + HousePriceModel.get_day_offset()

    def calculate_sale_day_by_day(self, year, month, day):
        """
        Calculates a sales day for a given year, month and day.
        :param year: The given year
        :param month: The given month
        :param day: The given day
        :return: A sales day
        """
        return (HousePriceModel.create_date(year, month, day) -
                self.get_base_date()).days + HousePriceModel.get_day_offset()

    @staticmethod
    def create_date(year, month, day):
        """
        Creates a pandas datetime object for a given year, month and day.
        :param year: The given year
        :param month: The given month
        :param day: The given day
        :return: A pandas datetime object corresponding to the given year,
        month and day
        """
        return pd.to_datetime(HousePriceModel.format_date(year, month, day),
                              format='%Y%m%d', errors='ignore')

    @staticmethod
    def create_model_feature(destination, source, name):
        """
        Creates a feature in a destination data frame.
        :param destination: The destination data frame
        :param source: The source data frame
        :param name: The name of the feature to copy
        :return: None
        """
        destination[name] = source[name]

    @staticmethod
    def format_date(year, month, day):
        """
        Formats a datetime string for a given year, month and day.
        :param year: The given year
        :param month: The given month
        :param day: The given day
        :return: A formatted datetime string
        """
        return '{:%Y%m%d}'.format(
            dt.datetime(year, month, day, 0, 0))

    def get_base_date(self):
        """
        Gets the base date.
        :return: The base date
        """
        return self.base_date

    @staticmethod
    def get_day_offset():
        """
        Gets the day offset for a sales day.
        :return: The day offset for a sales day
        """
        return 1

    def get_mean_response(self):
        """
        Gets the mean response for the model.
        :return: The mean response for the model
        """
        return self.mean_response

    def get_model(self):
        """
        Gets the model.
        :return: The model
        """
        return self.model

    def get_model_coefficients(self):
        return self.get_model().coef_

    def get_predictors(self):
        """
        Gets the model predictors.
        :return: The model predictors
        """
        return self.predictors

    def get_sales_data(self):
        """
        Gets raw sales data.
        :return: Raw sales data
        """
        return self.sales_data

    def get_scaler(self):
        """
        Gets the data scaler.
        :return: The scaler
        """
        return self.scaler

    def get_zip_code_dict(self):
        """
        Get the zip code dictionary.
        :return: The zip code dictionary
        """
        return self.zipcode_dict

    def initialize_model(self):
        """
        Initializes the model.  Call this before attempting to make a
        prediction!
        :return: None
        """
        self.read_housing_data()
        self.build_model()
        return None

    def look_up_zipcode_by_number(self, zipcode):
        """
        Looks up a zip code location code by numeric zip code.
        :param zipcode: The zip code
        :return: A zip code location code
        """
        return self.look_up_zipcode_by_string(str(zipcode))

    def look_up_zipcode_by_string(self, zipcode):
        """
        Looks up a zip code location code by string zip code.
        :param zipcode: The zip code
        :return: A zip code location code
        """
        zipcode_dict = self.get_zip_code_dict()
        if zipcode in zipcode_dict:
            return zipcode_dict.get(zipcode)[0]
        else:
            return np.nan

    def build_model(self):
        """
        Builds the model.
        :return: None
        """

        # Prepare the model data.  Isolate the response, and calculate its
        # mean.  Isolate the predictors.
        model_data = self.prepare_model_data()
        response = model_data.price
        self.mean_response = np.mean(response)
        self.predictors = model_data.drop('price', axis=1)

        # Prepare the predictors and response for modeling.
        x_for_model = self.get_scaler().fit_transform(self.get_predictors())
        y_for_model = np.array(response) - self.get_mean_response()

        # Fit the model.
        self.get_model().fit(X=x_for_model, y=y_for_model)
        return None

    def predict(self, features):
        """
        Makes a house price prediction.
        :param features: Features of the house.
        :return: A house price prediction
        """
        return self.get_model().predict(self.prepare_test_row(features))[0]\
               + self.get_mean_response()

    def prepare_model_data(self):
        """
        Prepares and returns model data.  Housing data must be read first using
        read_housing_data().
        :return: Model data
        """

        # Create an empty data frame.
        model_data = pd.DataFrame()

        # Extract the sales date as an integer relative to the base date.
        sales_data = self.get_sales_data()
        model_data['sale_day'] =\
            self.calculate_sale_day_by_date(sales_data['date'])

        # Create the other model features, including the location field.  The location
        # field is an integer based on zip code, which gives the relative average value
        # of homes in that zip code.
        HousePriceModel.create_model_feature(model_data, sales_data, 'price')
        HousePriceModel.create_model_feature(model_data, sales_data, 'bathrooms')
        HousePriceModel.create_model_feature(model_data, sales_data, 'sqft_living')
        HousePriceModel.create_model_feature(model_data, sales_data, 'sqft_lot')
        HousePriceModel.create_model_feature(model_data, sales_data, 'waterfront')
        HousePriceModel.create_model_feature(model_data, sales_data, 'view')
        HousePriceModel.create_model_feature(model_data, sales_data, 'condition')
        HousePriceModel.create_model_feature(model_data, sales_data, 'grade')
        model_data['location'] = np.vectorize(self.look_up_zipcode_by_string)\
            (sales_data['zipcode'].apply(str))
        return model_data

    def prepare_test_row(self, home_features):
        """
        Prepares a test row for prediction.
        :param home_features: A dictionary of home features
        :return: A row ready for price prediction
        """
        new_row = pd.DataFrame(home_features, index=[0])
        new_row = new_row[self.get_predictors().columns.tolist()]
        return self.get_scaler().transform(new_row)

    def read_housing_data(self):
        """
        Reads housing data.
        :return: None
        """

        # Construct the sales data path, and read the sales data.
        sales_data_path =\
            os.path.join(os.environ['SALES_DATA_PATH'], os.environ['SALES_DATA_FILE'])
        self.sales_data = pd.read_csv(sales_data_path, parse_dates=['date'])
        return None
