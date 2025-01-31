# This utility allows you to fetch latitude, longitude, and place details for given city/state
# combinations or zip codes using the OpenWeatherMap Geocoding API.

import requests
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeoLocationUtility:
    """Utility class to fetch latitude, longitude, and place details based on city/state or zip code."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/geo/1.0"

    def fetch_location_data(self, location):
        """Fetches location data based on city/state or zip code."""
        if ',' in location:  # City, State format (e.g., "Madison, WI, US")
            url = f"{self.base_url}/direct?q={location}&limit=1&appid={self.api_key}"
            response = requests.get(url)
        else:  # Zip code format
            url = f"{self.base_url}/zip?zip={location},US&appid={self.api_key}"
            response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Unable to fetch data for {location}. HTTP Status Code: {response.status_code}")
            return None

        data = response.json()
        if not data:
            print(f"No data found for {location}.")
            return None

        return data

    def display_location_data(self, location_data):
        """Displays the fetched location data."""
        if location_data:
            print(f"Location: {location_data.get('name', 'Unknown')}, {location_data.get('state', 'Unknown')}")
            print(f"Latitude: {location_data['lat']}")
            print(f"Longitude: {location_data['lon']}")
            print(f"Country: {location_data.get('country', 'Unknown')}")
            print("="*40)

    def process_locations(self, locations):
        """Process and display location data for multiple locations."""
        for location in locations:
            location_data = self.fetch_location_data(location)
            self.display_location_data(location_data)

class CommandLineInterface:
    """Handles command-line input and invokes the GeoLocationUtility."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Geolocation utility to fetch latitude, longitude, and place details.")
        self.parser.add_argument('--locations', nargs='+', help="City/State or Zip Code", required=True)
        self.api_key = os.getenv("API_KEY")  # API Key provided
        self.geo_util = GeoLocationUtility(api_key=self.api_key)

    def run(self):
        """Parses the command-line arguments and calls the appropriate methods."""
        args = self.parser.parse_args()
        self.geo_util.process_locations(args.locations)

if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run()