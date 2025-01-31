import pytest
from unittest.mock import patch
from geoloc_util import GeoLocationUtility


@pytest.fixture
def mock_city_data():
    return [{
        "name": "Madison",
        "state": "WI",
        "country": "US",
        "lat": 43.0731,
        "lon": -89.4012
    }]


@pytest.fixture
def mock_zip_data():
    return [{
        "name": "Schroon Lake",
        "state": "NY",
        "country": "US",
        "lat": 43.8833,
        "lon": -73.7167
    }]


# Test that the fetch_location_data function works with city/state input
@patch('requests.get')
def test_fetch_city_data(mock_get, mock_city_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_city_data

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("Madison, WI")
    assert result['name'] == "Madison"
    assert result['state'] == "WI"
    assert result['country'] == "US"
    assert result['lat'] == 43.0731
    assert result['lon'] == -89.4012


# Test that the fetch_location_data function works with zip code input
@patch('requests.get')
def test_fetch_zip_data(mock_get, mock_zip_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_zip_data

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("12345")
    assert result['name'] == "Schroon Lake"
    assert result['state'] == "NY"
    assert result['country'] == "US"
    assert result['lat'] == 43.8833
    assert result['lon'] == -73.7167


# Test that invalid city/state input returns None
@patch('requests.get')
def test_fetch_invalid_city_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("FakeCity, XX")
    assert result is None


# Test that invalid zip code returns None
@patch('requests.get')
def test_fetch_invalid_zip_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("99999")
    assert result is None


# Test that fetch_location_data raises an error for 500 status code
@patch('requests.get')
def test_fetch_location_data_500_error(mock_get):
    mock_get.return_value.status_code = 500
    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("Madison, WI")
    assert result is None


# Test that fetch_location_data handles empty response gracefully
@patch('requests.get')
def test_fetch_location_data_empty_response(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    result = geo_util.fetch_location_data("UnknownCity, XX")
    assert result is None


# Test that display_location_data correctly formats and prints results
@patch('requests.get')
@patch('builtins.print')
def test_display_location_data(mock_print, mock_get, mock_city_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_city_data

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    location_data = geo_util.fetch_location_data("Madison, WI")
    geo_util.display_location_data(location_data)
    mock_print.assert_called_with("Location: Madison, WI\nLatitude: 43.0731\nLongitude: -89.4012\nCountry: US\n========================================")


# Test process_locations correctly processes a list of locations
@patch('requests.get')
def test_process_multiple_locations(mock_get, mock_city_data, mock_zip_data):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [mock_city_data, mock_zip_data]

    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    geo_util.process_locations(["Madison, WI", "12345"])

    # Check that both locations are processed correctly
    assert mock_get.call_count == 2


# Test that process_locations handles no locations gracefully
@patch('requests.get')
def test_process_no_locations(mock_get):
    geo_util = GeoLocationUtility(api_key="f9c470fed8e9cb61aee1cfa567616f2e")
    geo_util.process_locations([])
    # No call should be made
    assert mock_get.call_count == 0