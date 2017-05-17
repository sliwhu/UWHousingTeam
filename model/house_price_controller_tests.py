"""
Contains unit tests for the house price controller.
"""
import unittest
from house_price_controller import create_test_frame
from house_price_controller import predict_using_forest
from house_price_controller import predict_using_ridge

# Constants
LOW_VALUE = 700000.
HIGH_VALUE = 1300000.


class MyTestCase(unittest.TestCase):
    """
    Contains unit tests for individual houses.
    """

    def test_house_one(self):
        """
        Performs a test house price prediction for 1817 N 51st St,
        Seattle, WA, 98103.

        :return: None
        """

        features = {'sale_year': 2017,
                    'sale_month': 6,
                    'sale_day': 1,
                    'bedrooms': 3,
                    'bathrooms': 2.5,
                    'sqft_living': 1430,
                    'sqft_lot': 3210,
                    'floors': 2,
                    'waterfront': 0,
                    'view': 0,
                    'condition': 5,
                    'grade': 6,
                    'sqft_above': 1430,
                    'sqft_basement': 0,
                    'yr_built': 1984,
                    'yr_renovated': 0,
                    'zipcode': 98103,
                    'latitude': 47.665556,
                    'longitude': -122.335604,
                    'list_price': 750000}

        house_frame = create_test_frame(features)
        price_by_forest = predict_using_forest(house_frame)
        price_by_ridge = predict_using_ridge(house_frame)
        self.assertTrue(LOW_VALUE <= price_by_forest <= HIGH_VALUE and
                        LOW_VALUE <= price_by_ridge <= HIGH_VALUE)

    def test_house_two(self):
        """
        Performs a test house price prediction for 5218 Greenwood Ave N,
        Seattle, WA, 98103.

        :return: None
        """

        features = {'sale_year': 2017,
                    'sale_month': 6,
                    'sale_day': 1,
                    'bedrooms': 4,
                    'bathrooms': 3.,
                    'sqft_living': 2640,
                    'sqft_lot': 3920,
                    'floors': 3,
                    'waterfront': 0,
                    'view': 0,
                    'condition': 5,
                    'grade': 6,
                    'sqft_above': 1990,
                    'sqft_basement': 650,
                    'yr_built': 1918,
                    'yr_renovated': 2007,
                    'zipcode': 98103,
                    'latitude': 47.666952,
                    'longitude': -122.355107,
                    'list_price': 1000000}

        house_frame = create_test_frame(features)
        price_by_forest = predict_using_forest(house_frame)
        price_by_ridge = predict_using_ridge(house_frame)
        self.assertTrue(LOW_VALUE <= price_by_forest <= HIGH_VALUE and
                        LOW_VALUE <= price_by_ridge <= HIGH_VALUE)


if __name__ == '__main__':
    unittest.main()
