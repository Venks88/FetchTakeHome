import unittest
from parameterized import parameterized
from geoloc_util import GeoLocationUtility


class TestGeoLocationUtility(unittest.TestCase):

    # Sample test data for parameterized tests
    @parameterized.expand([
        # Test 1: Empty location query, expected 400 error with message "Nothing to geocode"
        ("", [{'cod': '400', 'message': 'invalid zip code'}]),

        # Test 2: Valid location "Columbus, Ohio", expected to return a location object
        ("Columbus, Ohio", [
            {
                "name": "Columbus",
                "local_names": {
                    "ar": "كولومبوس", "en": "Columbus", "ru": "Колумбус",
                    "ta": "கொலம்பஸ்", "uk": "Колумбус", "he": "קולומבוס", "pl": "Columbus"
                },
                "lat": 39.9622601,
                "lon": -83.0007065,
                "country": "US",
                "state": "Ohio"
            }
        ]),

        # Test 3: Invalid location with empty query, expected empty list
        ("'''', ;;;;", None),

        # Test 4: Invalid location query with only empty quotes, expected empty list
        ("'''''", [{'cod': '404', 'message': 'not found'}]),

        # Test 5: Missing API key, expected 401 error (invalid API key)
        ("yellow", [{'cod': '404', 'message': 'not found'}]),

        # Test 6: Invalid location query ("yellowKings"), expected empty list
        ("yellowKings", [{'cod': '404', 'message': 'not found'}]),

        # Test 7: Valid location "yellow", expected to return a valid location (Yellow Springs)
        ("yellow", [{'cod': '404', 'message': 'not found'}]),

        # Test 8: Invalid zip code ("H9G1X6"), expected empty list
        ("H9G1X6", [{'cod': '404', 'message': 'not found'}])
    ])
    def test_fetch_location_data(self, location, expected_response):
        """Test the fetch_location_data method with different location inputs."""

        # Use a valid API key here
        api_key = 'f897a99d971b5eef57be6fafa0d83239'  # Replace with a valid API key
        geo_util = GeoLocationUtility(api_key)

        # Fetch the location data
        response = geo_util.fetch_location_data(location)

        # Assert the response matches the expected output
        self.assertEqual(response, expected_response)

    def test_fetch_state_from_lat_lon(self):
        """Test the fetch_state_from_lat_lon method with real data."""

        # Use a valid API key here
        api_key = 'f897a99d971b5eef57be6fafa0d83239'  # Replace with a valid API key
        geo_util = GeoLocationUtility(api_key)

        # Test with known lat/lon for Columbus, OH
        lat = [39.9622601]
        lon = [-83.0007065]

        state = geo_util.fetch_state_from_lat_lon(lat, lon)

        # Assert that the state returned is "Ohio"
        self.assertEqual(state, "Ohio")

    def test_fetch_location_data_invalid_key(self):
        """Test if the API returns a 401 status when there is no valid API key."""

        # Use an invalid API key here
        api_key = ''  # Empty or invalid API key
        geo_util = GeoLocationUtility(api_key)

        # Try fetching location data with the invalid key
        response = geo_util.fetch_location_data("yellow")

        # Assert that the response matches the expected error message
        self.assertEqual(response, [{'cod': 401, 'message': 'Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.'}])

if __name__ == '__main__':
    unittest.main()
