## FetchTakeHome
Fetch Take-Home Test

## Requirements:
- Python 3.x
- requests library
- pytest (for testing)


## Steps:
1. Install Dependencies: Install the necessary libraries (requests for making API calls, argparse for command-line parsing, pytest for testing).
2. Create Utility Function: This function will handle both city/state and zip code lookups. 
3. Command-Line Interface: We’ll use the argparse library to parse user input. 
4. API Communication: We will use Python’s requests library to communicate with the OpenWeatherMap API. 
5. Test the Utility: Create a suite of tests using Pytest.

## Gitlab Actions Job:
https://github.com/Venks88/FetchTakeHome/actions/runs/13092927440 -> Last one submitted.
The job has access of an HTML report for all tests run.

## Installation:
```bash
pip install --upgrade pip
pip install pytest
pip install python-dotenv
pip install requests
pip install pytest pytest-html
pip install pytest-cov
pip install -r Utility/requirements.txt
```

## Code Description:
**_Functions used and description:_**

1. API Key & URL: The API key provided is stored in the API_KEY variable, and the base URL for the API is BASE_URL. 
2. fetch_location_data: This function handles fetching the location data from the API. It checks if the input is a city/state or zip code. If it's a city/state combination, it calls the direct endpoint, and if it's a zip code, it calls the zip endpoint. 
3. display_location_data: After fetching the data, this function formats and prints the location details, including latitude, longitude, and place name. 
4. main: This function processes the locations provided by the user and prints the results for each location. 
5. argparse: The command-line argument parsing is handled by the argparse library, which allows the user to input multiple locations.

## Some easy tests to run:
**_This can be used to see if you have all the files and libraries required:_**

```bash
python ./Utility/geoloc_util.py --locations "123, MI"
python ./Utility/geoloc_util.py --locations "12345" "02135" "10001"
python ./Utility/geoloc_util.py --locations "12345" "02135" "10001"
python ./Utility/geoloc_util.py --locations "qweqeqeqwe,qweqweq"
python ./Utility/geoloc_util.py --locations "Columbus, OH"
python ./Utility/geoloc_util.py --locations "Columbus, OH" "Chicago, IL"
python ./Utility/geoloc_util.py --locations ";;;;;"
python ./Utility/geoloc_util.py --locations ""
python ./Utility/geoloc_util.py --locations "123123123123"
python ./Utility/geoloc_util.py --locations "12312"
python ./Utility/geoloc_util.py --locations "90210"
python ./Utility/geoloc_util.py --locations "9021090210"
python ./Utility/geoloc_util.py --locations "9 0 2 1 0"
python ./Utility/geoloc_util.py --locations "<<9 0 2 1 0>>"
python ./Utility/geoloc_util.py --locations "Columbus, OH" "Chicago, IL" "12345" "02135" "10001" "123123123123"
```

## Some local tests to run based of the command line:
**_Run this locally:_**
```bash
cd RunLocallyOnly
pytest test_geoloc_commandline.py -v
```

## Run all integration tests locally:
**_Run tests locally:_**
```bash
pytest ./Utility -v
```