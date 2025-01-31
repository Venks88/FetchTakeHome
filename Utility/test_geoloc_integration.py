import os
from geoloc_util import GeoLocationUtility
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_integration_valid_city_and_state():
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    result = geo_util.fetch_location_data("Madison, WI")
    assert result is not None
    assert result[0]['lat'] == 43.074761
    assert result[0]['lon'] == -89.3837613
    assert result[0]['country'] == 'US'
    assert result[0]['state'] == 'Wisconsin'
    assert result[0]['local_names']['en'] == 'Madison'
    assert result[0]['name'] == 'Madison'

def test_integration_valid_zip_code():
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    result = geo_util.fetch_location_data("12345")
    assert result is not None
    assert 'lat' in result
    assert 'lon' in result

def test_integration_invalid_city():
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    result = geo_util.fetch_location_data("InvalidCity, XX")
    assert result is None

def test_integration_invalid_zip():
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    result = geo_util.fetch_location_data("99999")
    assert result is None
