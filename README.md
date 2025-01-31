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

## Installation:
```bash
pip install python-dotenv
pip install -r Utility/requirements.txt
```

## Code Description:
**_Functions used and description:_**

1. API Key & URL: The API key provided is stored in the API_KEY variable, and the base URL for the API is BASE_URL. 
2. fetch_location_data: This function handles fetching the location data from the API. It checks if the input is a city/state or zip code. If it's a city/state combination, it calls the direct endpoint, and if it's a zip code, it calls the zip endpoint. 
3. display_location_data: After fetching the data, this function formats and prints the location details, including latitude, longitude, and place name. 
4. main: This function processes the locations provided by the user and prints the results for each location. 
5. argparse: The command-line argument parsing is handled by the argparse library, which allows the user to input multiple locations.