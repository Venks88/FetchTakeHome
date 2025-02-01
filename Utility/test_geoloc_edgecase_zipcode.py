import unittest
import os
from parameterized import parameterized
from geoloc_util import GeoLocationUtility  # Assuming your code is in geo_location_utility.py
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class TestGeoLocationUtilityZip(unittest.TestCase):

    # Sample test data for parameterized tests
    @parameterized.expand([
        # Test 1: Valid zip code (12345), should return location data for Schenectady
        ("12345", [{
            "zip": "12345",
            "name": "Schenectady",
            "lat": 42.8142,
            "lon": -73.9396,
            "country": "US"
        }]),

        # Test 2: Invalid zip code (234), should return 404 error with message "not found"
        ("234", [{"cod": "404", "message": "not found"}]),

        # Test 3: Empty zip code, should return a 400 error with message "Nothing to geocode"
        ("", [{"cod": "400", "message": "invalid zip code"}]),

        # Test 4: Invalid zip with special characters (<<%12345%>>), should return 500 internal error
        ("<<%12345%>>", [{'cod': '404', 'message': 'not found'}]),

        # Test 5: Invalid zip with some encoded characters (12<<>>345), should return location data for Schenectady
        ("12%3C%3C%3E%3E345", [{
            "zip": "12345",
            "name": "Schenectady",
            "lat": 42.8142,
            "lon": -73.9396,
            "country": "US"
        }]),

        # Test 6: Non-existent zip code (100010), should return 404 error with message "not found"
        ("100010", [{"cod": "404", "message": "not found"}]),

        # Test 7: Invalid zip code "PPPPP", should return 404 error with message "not found"
        ("PPPPP", [{"cod": "404", "message": "not found"}]),

        # Test 8: Non-existent zip code (12341), should return 404 error with message "not found"
        ("12341", [{"cod": "404", "message": "not found"}]),

    ])
    def test_fetch_zip_location_data(self, zip_code, expected_response):
        """Test the fetch_location_data method with different zip code inputs."""

        # Use a valid API key here
        api_key = os.getenv("API_KEY")  # Replace with a valid API key
        geo_util = GeoLocationUtility(api_key)

        # Fetch the location data using the provided zip code
        response = geo_util.fetch_location_data(zip_code)

        # Assert that the response matches the expected output
        self.assertEqual(response, expected_response)

    def test_fetch_location_data_invalid_key(self):
        """Test if the API returns a 401 status when there is no valid API key for a zip code."""

        # Use an invalid API key here
        api_key = ''  # Empty or invalid API key
        geo_util = GeoLocationUtility(api_key)

        # Try fetching location data with the invalid key
        response = geo_util.fetch_location_data("02135")

        # Expected result is an error message indicating the invalid API key
        expected_response = [{"cod": 401, "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}]

        # Assert that the response matches the expected error message
        self.assertEqual(response, expected_response)

if __name__ == '__main__':
    unittest.main()
