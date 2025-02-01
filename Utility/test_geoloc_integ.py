import os
import subprocess
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from geoloc_util import GeoLocationUtility  # Adjust the import if necessary


class TestGeoLocationUtility(unittest.TestCase):

    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

    def test_integration_multi_zipcode(self):
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

    def test_integration_multi_location(self):
        test_data = [
            {'country': 'US', 'lat': 39.9622601, 'local_names': {'ar': 'كولومبوس', 'en': 'Columbus', 'pl': 'Columbus', 'ru': 'Колумбус', 'ta': 'கொலம்பஸ்', 'uk': 'Колумбус'}, 'lon': -83.0007065, 'name': 'Columbus', 'state': 'Ohio'},
            {'name': 'Boston', 'local_names': {'ru': 'Бостон', 'fr': 'Boston', 'nl': 'Boston', 'fi': 'Boston', 'de': 'Boston', 'ro': 'Boston', 'pt': 'Boston', 'es': 'Boston', 'sv': 'Boston', 'ja': 'ボストン', 'ga': 'Bostún', 'ar': 'بوسطن', 'zh': '波士顿', 'he': 'בוסטון', 'sr': 'Бостон', 'oc': 'Boston', 'en': 'Boston', 'it': 'Boston', 'fa': 'بوستون', 'mk': 'Бостон', 'uk': 'Бостон', 'pl': 'Boston', 'ko': '보스턴', 'eo': 'Bostono', 'bn': 'বোস্টন', 'ta': 'பாஸ்டன்'}, 'lat': 42.3554334, 'lon': -71.060511, 'country': 'US', 'state': 'Massachusetts'},
            {'name': 'San Diego', 'local_names': {'uk': 'Сан-Дієго', 'ar': 'سان دييغو', 'en': 'San Diego', 'lt': 'San Diegas', 'zh': '聖地牙哥', 'ko': '샌디에이고', 'he': 'סן דייגו', 'ja': 'サンディエゴ', 'ru': 'Сан-Диего', 'pt': 'São Diego', 'oc': 'San Diego'}, 'lat': 32.7174202, 'lon': -117.1627728, 'country': 'US', 'state': 'California'}
        ]

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Test with multiple locations
        locations = ["Columbus, OH", "Boston, MA", "San Diego, CA"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[0]['lat'], test_data[location]['lat'], f"Location name mismatch for {locations[location]}")
            self.assertEqual(result[0]['lon'], test_data[location]['lon'], f"Location name mismatch for {locations[location]}")

    def test_integration_single_zipcode(self):
        test_data = [
            {'country': 'US', 'lat': 40.2845, 'lon': -82.284, 'name': 'Clay Township', 'zip': '43005'}
        ]

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Test with multiple locations
        locations = ["43005"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[0]['lat'], test_data[location]['lat'], f"Location name mismatch for {locations[location]}")
            self.assertEqual(result[0]['lon'], test_data[location]['lon'], f"State mismatch for {locations[location]}")

    def test_integration_single_invalidzipcode(self):
        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Test with multiple locations
        locations = [";;;;;"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should be None for {locations[location]}")
            self.assertEqual(result, [{'cod': '404', 'message': 'not found'}])

    def test_integration_single_location(self):
        test_data = [{'country': 'US', 'lat': 39.9622601, 'local_names': {'ar': 'كولومبوس', 'en': 'Columbus', 'pl': 'Columbus', 'ru': 'Колумбус', 'ta': 'கொலம்பஸ்', 'uk': 'Колумбус'}, 'lon': -83.0007065, 'name': 'Columbus', 'state': 'Ohio'}]

        # Instantiate the GeoLocationUtility with a mock API key
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Test with multiple locations
        locations = ["Columbus, OH"]
        for location in range(len(locations)):
            result = geo_util.fetch_location_data(locations[location])
            self.assertIsNotNone(result, f"Result should not be None for {locations[location]}")
            self.assertEqual(result[0]['lat'], test_data[location]['lat'], f"Location name mismatch for {locations[location]}")
            self.assertEqual(result[0]['lon'], test_data[location]['lon'], f"Location name mismatch for {locations[location]}")

    def test_geolocation_output_multi_location(self):
        # Input locations
        locations = ["Columbus, OH", "Chicago, IL"]

        # Run the command as a subprocess
        command = ["python", "geoloc_util.py", "--locations"] + locations
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Get the output of the command
        output = result.stdout

        # Expected Output structure
        expected_output = (
                "Location: Columbus, Ohio\n"
                "Latitude: 39.9622601\n"
                "Longitude: -83.0007065\n"
                "Country: US\n"
                "========================================\n"
                 "Location: Chicago, Illinois\n"
                 "Latitude: 41.8755616\n"
                 "Longitude: -87.6244212\n"
                 "Country: US\n"
                "========================================\n"
        )

        # Assert the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_geolocation_output_multi_zipcode(self):
        # Input locations
        locations = ["01235", "54636"]

        # Run the command as a subprocess
        command = ["python", "geoloc_util.py", "--locations"] + locations
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command ran successfully
        self.assertEqual(result.returncode, 0)

        # Get the output of the command
        output = result.stdout

        # Expected Output structure
        expected_output = (
            "Location: Peru, Massachusetts\n"
            "Latitude: 42.4298\n"
            "Longitude: -73.0724\n"
            "Country: US\n"
            "========================================\n"
            "Location: Town of Onalaska, Wisconsin\n"
            "Latitude: 43.9761\n"
            "Longitude: -91.2497\n"
            "Country: US\n"
            "========================================\n"
        )

        # Assert the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_geolocation_zipcode_with_invalid(self):
        # Input locations
        locations = ["01235", ";;;;;"]

        # Run the command as a subprocess
        command = ["python", "geoloc_util.py", "--locations"] + locations
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command ran successfully
        self.assertEqual(result.returncode, 0)

        # Get the output of the command
        output = result.stdout

        # Expected Output structure
        expected_output = (
            "Location: Peru, Massachusetts\n"
            "Latitude: 42.4298\n"
            "Longitude: -73.0724\n"
            "Country: US\n"
            "========================================\n"
            "Location: Unknown, [{'cod': '400', 'message': 'Nothing to geocode'}]\n"
            'Latitude: Unknown\n'
            'Longitude: Unknown\n'
            'Country: Unknown\n'
            '========================================\n'
        )

        # Assert the output matches the expected output
        self.assertEqual(output, expected_output)

    def test_special_characters_in_location(self):
        # Test with cities that have special characters in their names
        locations = ["San José, CA", "São Paulo, SP"]
        result = self.geo_util.fetch_location_data(locations[0])
        self.assertIsNotNone(result)
        result = self.geo_util.fetch_location_data(locations[1])
        self.assertIsNotNone(result)

    def test_api_key_rate_limiting(self):
        os.environ["API_KEY"] = os.getenv("API_KEY")  # Simulate missing API key
        result = self.geo_util.fetch_location_data("10001")  # Some location
        self.assertIsNotNone(result)  # Ensure it fails gracefully

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_location_data_valid(self, mock_stdout):
        # Mock valid location data
        location_data = [
            {
                'name': 'New York',
                'state': 'New York',
                'lat': 40.7484,
                'lon': -73.9967,
                'country': 'US'
            }
        ]

        geo_util = GeoLocationUtility(api_key="mocked_api_key")
        geo_util.display_location_data(location_data)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Expected output for the given data
        expected_output = (
            "Location: New York, New York\n"
            "Latitude: 40.7484\n"
            "Longitude: -73.9967\n"
            "Country: US\n"
            "========================================\n"
        )

        # Check if the output matches
        self.assertEqual(output.strip(), expected_output.strip())

    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(GeoLocationUtility, 'fetch_state_from_lat_lon', return_value="New York")
    def test_display_location_data_missing_state(self, mock_fetch_state, mock_stdout):
        # Mock location data with missing 'state'
        location_data = [
            {
                'name': 'Unknown City',
                'state': 'Unknown',  # State is missing
                'lat': 40.7484,
                'lon': -73.9967,
                'country': 'US'
            }
        ]

        geo_util = GeoLocationUtility(api_key="mocked_api_key")
        geo_util.display_location_data(location_data)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Expected output for the given data, with the state being fetched as "New York"
        expected_output = (
            "Location: Unknown City, New York\n"
            "Latitude: 40.7484\n"
            "Longitude: -73.9967\n"
            "Country: US\n"
            "========================================\n"
        )

        # Check if the output matches
        self.assertEqual(output.strip(), expected_output.strip())
        mock_fetch_state.assert_called_once_with({40.7484}, {-73.9967})  # Ensure the fetch_state_from_lat_lon method was called

    @patch('requests.get')
    def test_make_api_request_empty_data(self, mock_get):
        # Simulate an empty response (empty JSON data)
        mock_response = MagicMock()
        mock_response.json.return_value = []  # Empty data list
        mock_response.raise_for_status = MagicMock()  # Mock the raise_for_status method to do nothing

        # Mock the requests.get to return this response
        mock_get.return_value = mock_response

        geo_util = GeoLocationUtility(api_key="mocked_api_key")

        # Call the private _make_api_request method
        result = geo_util._make_api_request("http://mockedurl.com")

        # Assert that the result is None (because the data is empty)
        self.assertIsNone(result)

        # Check if the print statement was called with the correct message
        log = geo_util._make_api_request("http://mockedurl.com")
        self.assertIsNone(log)


    def test_fetch_state_from_lat_lon(self):
        city = self.geo_util.fetch_state_from_lat_lon([40.7484],[-73.9967])
        self.assertEqual(city, "New York")

        city = self.geo_util.fetch_state_from_lat_lon([""], ["-73.9967"])
        self.assertIsNotNone(city)
        self.assertEqual(city, [{'cod': '400', 'message': 'Nothing to geocode'}])

        city = self.geo_util.fetch_state_from_lat_lon(["123.123"], [""])
        self.assertIsNotNone(city)
        self.assertEqual(city, [{'cod': '400', 'message': 'Nothing to geocode'}])

        city = self.geo_util.fetch_state_from_lat_lon([""], [""])
        self.assertIsNotNone(city)
        self.assertEqual(city, [{'cod': '400', 'message': 'Nothing to geocode'}])


if __name__ == "__main__":
    unittest.main()