import os
import subprocess
import unittest
from geoloc_util import GeoLocationUtility  # Adjust the import if necessary


class TestGeoLocationUtility(unittest.TestCase):

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
            self.assertIsNone(result, f"Result should be None for {locations[location]}")

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

        # Check if the command ran successfully
        self.assertEqual(result.returncode, 0)

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
            "Request failed: 404 Client Error: Not Found for url: http://api.openweathermap.org/geo/1.0/zip?zip=;;;;;,US&appid=f897a99d971b5eef57be6fafa0d83239\nError: Unable to fetch data for ;;;;;.\n"
        )

        # Assert the output matches the expected output
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
