"""
Contains unit tests for the 2nd house price model.
"""
import unittest
from house_price_model_2 import HousePriceModel

# Constants
LOW_VALUE = 400000.
HIGH_VALUE = 1200000.

# Note: It is expected that the following environment variables will be
# set so that the house price model will be able to locate its training
# data:
#
# SALES_DATA_PATH:  The path of the sales data training file, e.g.: "~/directory"
# SALES_DATA_FILE:  The name of the sales data training file, e.g.: "File.csv"


class MyTestCase(unittest.TestCase):
    """
    Contains unit tests for individual houses for the 2nd house price model.
    """

    def __init__(self, *args, **kwargs):
        super(MyTestCase, self).__init__(*args, **kwargs)
        self.house_price_model = HousePriceModel()
        self.house_price_model.initialize_model()

    def test_house_one(self):
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
        prediction = self.house_price_model.predict(features)
        self.assertTrue(LOW_VALUE <= prediction <= HIGH_VALUE and
                        LOW_VALUE <= prediction <= HIGH_VALUE)

    def test_house_two(self):
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
        prediction = self.house_price_model.predict(features)
        self.assertTrue(LOW_VALUE <= prediction <= HIGH_VALUE and
                        LOW_VALUE <= prediction <= HIGH_VALUE)


if __name__ == '__main__':
    unittest.main()
