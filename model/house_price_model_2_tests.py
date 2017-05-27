"""
Contains unit tests for the 2nd house price model.
"""
import unittest

import pandas as pd
from dateutil.parser import parse
from house_price_model_2 import HousePriceModel
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing.data import StandardScaler

# Note: It is expected that the following environment variables will be
# set so that the house price model will be able to locate its training
# data:
#
# SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
# SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"


class MyTestCase(unittest.TestCase):
    """
    Contains unit tests for the 2nd house price model.

    The following methods in HousingPriceModel do not have independent tests
    here, and are presumed to be sufficiently tested from calls through the
    other unit tests:

    1. initialize_model
    2. build_model
    3. prepare_model_data
    4. prepare_test_row
    5. read_housing_data
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the unit test class.
        :param args: Argument for unittest.TestCase
        :param kwargs: Argument for unittest.TestCase
        """
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.house_price_model = HousePriceModel()
        self.house_price_model.initialize_model()
        self.price_accuracy = 100.

    def test_calculate_sales_by_date(self):
        """
        Tests HousePriceModel.calculate_sales_day_by_date.
        :return: True or False
        """

        # Declare and initialize a tuple of test dates.
        dates = (self.house_price_model.create_date(2014, 1, 1),
                 self.house_price_model.create_date(2014, 1, 2),
                 self.house_price_model.create_date(2014, 1, 31),
                 self.house_price_model.create_date(2014, 2, 1),
                 self.house_price_model.create_date(2014, 2, 28),
                 self.house_price_model.create_date(2014, 3, 1),
                 self.house_price_model.create_date(2015, 1, 1),
                 self.house_price_model.create_date(2016, 1, 1),
                 self.house_price_model.create_date(2016, 2, 29),
                 self.house_price_model.create_date(2016, 3, 1))

        # Declare and initialize the expected results of the test dates
        # conversion.  Convert the test dates.
        expected = (1, 2, 31, 32, 59, 60, 366, 731, 790, 791)
        received = self.house_price_model.calculate_sale_day_by_date\
            (pd.Series(dates))

        # Assert that all received test dates match their expected values.
        return self.assertListEqual(received.tolist(),
                                    list(expected))

    def test_calculate_sales_by_day(self):
        """
        Tests HousePriceModel.calculate_sales_day_by_day.
        :return: True or False
        """
        return self.assertTrue(
            self.house_price_model.calculate_sale_day_by_day(
                2016, 2, 29) == 790)

    def test_can_predict(self):
        """
        Tests HousePriceModel.can_predict.
        :return: True or False
        """
        return self.assertTrue(self.house_price_model.can_predict)

    def test_create_date(self):
        """
        Tests HousePriceModel.create_date.
        :return: True or False
        """

        # Declare and initialize a test year, month and day.
        year = 2017
        month = 7
        day = 4

        # Create the date object, and assert all resulting fields are what we
        # expect.
        date = HousePriceModel.create_date(year, month, day)
        self.assertTrue(date.year == year and
                        date.month == month and
                        date.day == day)

    def test_create_model_features(self):
        """
        Tests HousePriceModel.create_model_features.
        :return: True or False
        """

        # Declare and initialize the column name to use for the test, and a
        # series of column values.
        column_name = 'column'
        column_values = pd.Series((1, 2, 3, 4, 5))

        # Declare and initialize the source data frame, and give it the test
        # column and column values.
        source = pd.DataFrame()
        source[column_name] = column_values

        # Declare and initialize the destination date frame, and copy the
        # source column and values.
        destination = pd.DataFrame()
        HousePriceModel.create_model_feature(destination, source,
                                             column_name)

        # Get the destination values from the destination, and assert that all
        # received values match their expected values.
        destination_values = destination[column_name]
        return self.assertListEqual(destination_values.tolist(),
                                    column_values.tolist())

    def test_format_date(self):
        """
        Tests HousePriceModel.format_date.
        :return: True or False
        """

        # Declare and initialize a test year, month and day.
        year = 2020
        month = 2
        day = 29

        # Format the date, then parse it.
        date = HousePriceModel.format_date(year, month, day)
        parsed_date = parse(date)

        # Insure that the parsed date matches the expected values.
        return self.assertTrue(parsed_date.year == year and
                               parsed_date.month == month and
                               parsed_date.day == day)

    def test_get_base_date(self):
        """
        Tests HousePriceModel.get_base_date.
        :return: True or False
        """

        # Declare and initialize a test year, month and day.
        year = 2014
        month = 1
        day = 1

        # Insure that the base date matches the expected values.
        base_date = self.house_price_model.get_base_date()
        return self.assertTrue(base_date.year == year and
                               base_date.month == month and
                               base_date.day == day)

    def test_get_day_offset(self):
        """
        Tests HousePriceModel.get_day_offset.
        :return: True of False
        """
        self.assertTrue(HousePriceModel.get_day_offset() == 1)

    def test_get_mean_response(self):
        """
        Tests HousePriceModel.get_mean_response.
        :return: True or False
        """
        return self.assertAlmostEqual(self.house_price_model.get_mean_response(),
                                      537798., delta=self.price_accuracy)

    def test_get_model(self):
        """
        Tests HousePriceModel.get_model.
        :return: True or False
        """

        # Test whether the model is a RidgeCV model, and whether
        # the coefficients from the model match.
        model = self.house_price_model.get_model()
        return self.assertTrue(isinstance(model, RidgeCV)) \
               and self.assertListEqual(list(model.coef_),
                                        list(self.house_price_model.get_model_coefficients()))

    def test_get_model_coefficients(self):
        """
        Tests HousePriceModel.get_model.
        :return: True or False
        """

        # Just run the same test as the one for the model itself.
        return self.test_get_model()

    def test_get_predictors(self):
        """
        Tests HousePriceModel.get_predictors.
        :return: True or False
        """
        return self.assertTrue(
            self.house_price_model.get_predictors().shape[1] == 9)

    def test_get_sales_data(self):
        """
        Tests HousePriceModel.get_sales_data.
        :return: True or False
        """
        return self.assertTrue(
            len(self.house_price_model.get_sales_data().columns) == 22)

    def test_get_scaler(self):
        """
        Tests HousePriceModel.get_scaler.
        :return: True or False
        """
        return self.assertTrue(isinstance(
            self.house_price_model.get_scaler(), StandardScaler))

    def test_get_zip_code_dict(self):
        """
        Tests HousePriceModel.get_zip_code_dict.
        :return: True or False
        """
        return self.assertTrue(isinstance(
            self.house_price_model.get_zip_code_dict(), dict))

    def test_lookup_zipcode_by_number(self):
        """
        Tests HousePriceModel.lookup_zip_code_by_number.
        :return: True or False
        """

        # Declare and initialize the zip codes tuple.
        zip_codes = (98002, 98168, 98032, 98001, 98148, 98023, 98188, 98003, 98030, 98031,
                     98198, 98055, 98178, 98042, 98022, 98106, 98092, 98058, 98108, 98146,
                     98038, 98133, 98118, 98056, 98155, 98126, 98019, 98014, 98028, 98166,
                     98125, 98070, 98011, 98059, 98034, 98065, 98136, 98072, 98117, 98107,
                     98103, 98144, 98029, 98027, 98007, 98116, 98115, 98122, 98052, 98008,
                     98177, 98053, 98077, 98074, 98075, 98199, 98033, 98005, 98119, 98006,
                     98105, 98109, 98102, 98112, 98040, 98004)

        # Declare and initialize the locations tuple.
        locations = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                     40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                     50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                     60, 61, 62, 63, 64, 65)

        # Assert that lookup_zipcode_by_number returns the right value for
        # each zip code.
        return self.assertListEqual(
            [self.house_price_model.look_up_zipcode_by_number(zipcode)
             for zipcode in zip_codes], list(locations))

    def test_lookup_zipcode_by_string(self):
        """
        Tests HousePriceModel.lookup_zip_code_by_string.
        :return: True or False
        """

        # Declare and initialize the zip codes tuple.
        zip_codes = ('98002', '98168', '98032', '98001', '98148',
                     '98023', '98188', '98003', '98030', '98031',
                     '98198', '98055', '98178', '98042', '98022',
                     '98106', '98092', '98058', '98108', '98146',
                     '98038', '98133', '98118', '98056', '98155',
                     '98126', '98019', '98014', '98028', '98166',
                     '98125', '98070', '98011', '98059', '98034',
                     '98065', '98136', '98072', '98117', '98107',
                     '98103', '98144', '98029', '98027', '98007',
                     '98116', '98115', '98122', '98052', '98008',
                     '98177', '98053', '98077', '98074', '98075',
                     '98199', '98033', '98005', '98119', '98006',
                     '98105', '98109', '98102', '98112', '98040',
                     '98004')

        # Declare and initialize the locations tuple.
        locations = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                     10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                     20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                     30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                     40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                     50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                     60, 61, 62, 63, 64, 65)

        # Assert that lookup_zipcode_by_number returns the right value for
        # each zip code.
        return self.assertListEqual(
            [self.house_price_model.look_up_zipcode_by_string(zipcode)
             for zipcode in zip_codes], list(locations))

    def test_prediction_one(self):
        """
        Performs a test house price prediction for 1817 N 51st St,
        Seattle, WA, 98103.
        :return: None
        """

        # Declare and initialize a test row.
        features = {'sale_day':
                        self.house_price_model.calculate_sale_day_by_day(2017, 7, 1),
                    'bathrooms': 2.5,
                    'sqft_living': 1430,
                    'sqft_lot': 3210,
                    'waterfront': 0,
                    'view': 0,
                    'condition': 5,
                    'grade': 6,
                    'location':
                        self.house_price_model.look_up_zipcode_by_string('98103')
                   }

        # Make a prediction and check it.
        return self.assertAlmostEqual(self.house_price_model.predict(features),
                                      546596., delta=self.price_accuracy)

    def test_prediction_two(self):
        """
        Performs a test house price prediction for 5218 Greenwood Ave N,
        Seattle, WA, 98103.
        :return: None
        """

        # Declare and initialize a test row.
        features = {'sale_day':
                        self.house_price_model.calculate_sale_day_by_day(2017, 7, 1),
                    'bathrooms': 3,
                    'sqft_living': 2640,
                    'sqft_lot': 3920,
                    'waterfront': 0,
                    'view': 0,
                    'condition': 5,
                    'grade': 6,
                    'location':
                        self.house_price_model.look_up_zipcode_by_string('98103')
                   }

        # Make a prediction and check it.
        return self.assertAlmostEqual(self.house_price_model.predict(features),
                                      740494., delta=self.price_accuracy)

    def test_prediction_three(self):
        """
        Performs a test house price prediction for 216 Pike St SE,
        Auburn, WA 98002
        :return: None
        """

        # Declare and initialize a test row.
        features = {'sale_day':
                        self.house_price_model.calculate_sale_day_by_day(2017, 7, 1),
                    'bathrooms': 1,
                    'sqft_living': 1060,
                    'sqft_lot': 8000,
                    'waterfront': 0,
                    'view': 0,
                    'condition': 5,
                    'grade': 6,
                    'location':
                        self.house_price_model.look_up_zipcode_by_string('98002')
                   }

        # Make a prediction and check it.
        return self.assertAlmostEqual(self.house_price_model.predict(features),
                                      197570., delta=self.price_accuracy)


if __name__ == '__main__':
    unittest.main()
