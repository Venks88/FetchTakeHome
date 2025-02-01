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

    def fetch_state_from_lat_lon(self, lat, lon):
        url = f"{self.base_url}/reverse?lat={list(lat)[0]}&lon={list(lon)[0]}&limit=1&appid={self.api_key}"

        # Make the API request
        response = self._make_api_request(url)
        if not response:
            print(f"Error: Unable to fetch data for {lat} , {lon}.")
            return None

        if any('message' in item for item in response):
            return [response]
        else:
            if len(response) > 0:
                return response
            else:
                # Ensure the return format is always a list
                return response[0]['state'] or "Unknown"

    def fetch_location_data(self, location):
        """Fetches location data based on city/state or zip code."""

        if ',' in location:  # City, State format
            city, state_code = map(str.strip, location.split(','))
            state = self.get_statecode_from_state(state_code)
            location = f"{city}, {state}"
            url = f"{self.base_url}/direct?q={location}&limit=1&appid={self.api_key}"

        else:  # Assume zip code format
            url = f"{self.base_url}/zip?zip={location},US&appid={self.api_key}"

        # Make the API request
        response = self._make_api_request(url)

        if not response or len(response) == 0:
            print(f"No location data found for {location}")
            return None

        # Ensure the return format is always a list
        return [response] if isinstance(response, dict) else response

    def _make_api_request(self, url):
        """Helper function to make API request and handle errors."""
        try:
            response = requests.get(url, timeout=30) # 10 seconds timeout in case the url is down.s
            data = response.json()

            if not data:
                print(f"No data found for {url}.")
                return None

            return data

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def display_location_data(self, location_data):
        """Displays the fetched location data."""
        if location_data:
            for data in location_data:
                if data.get('state', 'Unknown') == 'Unknown':
                    state = self.fetch_state_from_lat_lon({data.get('lat', 'Unknown')}, {data.get('lon', 'Unknown')})
                    data['state'] = state
                print(f"Location: {data.get('name', 'Unknown')}, {data.get('state', 'Unknown')}")
                print(f"Latitude: {data.get('lat', 'Unknown')}")
                print(f"Longitude: {data.get('lon', 'Unknown')}")
                print(f"Country: {data.get('country', 'Unknown')}")
                print("="*40)

    def process_locations(self, locations):
        """Process and display location data for multiple locations."""
        for location in locations:
            location_data = self.fetch_location_data(location)
            self.display_location_data(location_data)

    def get_statecode_from_state(self, code):
        us_states = {
            "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
            "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
            "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
            "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
            "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
            "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
            "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
            "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
            "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
            "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
            "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
            "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
            "WI": "Wisconsin", "WY": "Wyoming"
        }

        if code not in us_states:
            return ValueError(f"Invalid State Code: {code}")
        else:
            return us_states.get(code, "Invalid State Code")

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