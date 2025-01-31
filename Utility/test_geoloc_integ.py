import os
import unittest
from geoloc_util import GeoLocationUtility  # Adjust the import if necessary


class TestGeoLocationUtility(unittest.TestCase):

    def test_integration_multi_Zipcode(self):
        test_data = [
            {'country': 'US', 'lat': 40.2845, 'lon': -82.284, 'name': 'Clay Township', 'zip': '43005'},
            {'country': 'US', 'lat': 42.3478, 'lon': -71.1566, 'name': 'Boston', 'zip': '02135'},
            {'country': 'US', 'lat': 40.7484, 'lon': -73.9967, 'name': 'New York', 'zip': '10001'}
        ]

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Test with multiple locations
        locations = ["43005", "02135", "10001"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[0]['lat'], test_data[location]['lat'], f"Location name mismatch for {locations[location]}")
            self.assertEqual(result[0]['lon'], test_data[location]['lon'], f"State mismatch for {locations[location]}")

if __name__ == "__main__":
    unittest.main()
