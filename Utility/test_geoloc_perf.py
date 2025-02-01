import pytest
from geoloc_util import GeoLocationUtility
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.mark.benchmark(group="performance")
def test_benchmark_multiple_city_requests(benchmark):
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    locations = ["Madison, WI", "Chicago, IL", "New York, NY", "Los Angeles, CA", "San Francisco, CA"]

    # Benchmark the process_locations method with a large number of requests
    benchmark(lambda: geo_util.process_locations(locations))

@pytest.mark.benchmark(group="performance")
def test_benchmark_large_zip_codes(benchmark):
    geo_util = GeoLocationUtility(api_key=os.getenv("API_KEY"))
    zip_codes = ["12345", "10001", "94105", "60601", "30303"]

    # Benchmark the process_locations method with a large number of zip codes
    benchmark.pedantic(lambda: geo_util.process_locations(zip_codes))
