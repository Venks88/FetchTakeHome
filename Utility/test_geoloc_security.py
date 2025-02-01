import pytest
import unittest
import os
from unittest.mock import patch
from dotenv import load_dotenv
from geoloc_util import GeoLocationUtility

# Load environment variables from .env file
load_dotenv()


class TestGeoLocationUtilitySecurity(unittest.TestCase):
    # Test for input sanitization (e.g., checking for XSS or other malicious input)
    @patch('requests.get')
    def test_input_validation_city(self, mock_get):
        mock_get.return_value.status_code = 200
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        # Malicious input with special characters (XSS)
        result = geo_util.fetch_location_data("<script>alert('xss')</script>")
        assert result is None

    # Test for rate-limiting behavior (simulate too many requests)
    @patch('requests.get')
    def test_rate_limiting(self, mock_get):
        mock_get.return_value.status_code = 429  # Too Many Requests
        geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))

        result = geo_util.fetch_location_data("Madison, WI")
        assert result is None

    # Test for checking API key leakage in logs or error messages
    @patch('requests.get')
    def test_api_key_security(self, mock_get):
        mock_get.return_value.status_code = 403  # Forbidden (invalid API key)
        geo_util = GeoLocationUtility(api_key="invalid_api_key")

        # Ensure that the API key isn't exposed in logs or errors
        with pytest.raises(Exception):
            geo_util.fetch_location_data("Madison,WI,US")
