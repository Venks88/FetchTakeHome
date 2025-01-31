import os
import unittest
from unittest.mock import patch
from geoloc_util import GeoLocationUtility  # Adjust the import if necessary

class TestGeoLocationUtility(unittest.TestCase):

    @patch('requests.get')
    def test_integration_multi_location(self, mock_get):
        # Mock response data for the locations
        mock_response = [
            {
                "name": "Madison",
                "state": "Michigan",
                "lat": 42.2808,
                "lon": -83.743,
                "country": "US"
            },
            {
                "name": "Boston",
                "state": "Massachusetts",
                "lat": 42.3601,
                "lon": -71.0589,
                "country": "US"
            },
            {
                "name": "Chicago",
                "state": "Illinois",
                "lat": 41.8781,
                "lon": -87.6298,
                "country": "US"
            }
        ]

        # Mock the return value of requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key="mock_api_key")

        # Test with multiple locations
        locations = ["Madison, MI", "Boston, MA", "Chicago, IL"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[location]['name'], locations[location].split(',')[0], f"Location name mismatch for {locations[location]}")
            state = geo_util.get_statecode_from_state(locations[location].split(',')[1].strip())
            self.assertEqual(result[location]['state'], state, f"State mismatch for {locations[location]}")

    @patch('requests.get')
    def test_integration_multi_Zipcode(self, mock_get):
        # Mock response data for the locations
        mock_response = [
            {'name': 'Madison', 'state': 'Michigan', 'lat': 42.2808, 'lon': -83.743, 'country': 'US'},
            {'name': 'Boston', 'state': 'Massachusetts', 'lat': 42.3601, 'lon': -71.0589, 'country': 'US'},
            {'name': 'Chicago', 'state': 'Illinois', 'lat': 41.8781, 'lon': -87.6298, 'country': 'US'}
        ]

        # Mock the return value of requests.get
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key="mock_api_key")

        # Test with multiple locations
        locations = ["12345", "02135", "10001"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[location]['lat'], mock_response[location]['lat'], f"Location name mismatch for {locations[location]}")
            self.assertEqual(result[location]['lon'], mock_response[location]['lon'], f"State mismatch for {locations[location]}")

if __name__ == "__main__":
    unittest.main()
