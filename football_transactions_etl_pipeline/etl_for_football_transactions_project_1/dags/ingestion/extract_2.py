import pandas as pd
import requests


def get_results(api_url="http://api.football-data.org/v4/competitions/"):
    """
    A generic function that retrieves data from a given API.
    Args:
        api_url (str): The API endpoint URL.
    Returns:
        DataFrame: API data normalized into a pandas DataFrame.
    """
    api_info = requests.get(api_url)
    if api_info.status_code == 200:
        api_data = api_info.json()
    else:
        print("Error in fetching data from the API provided")
        return pd.DataFrame()

    df = pd.json_normalize(api_data["competitions"])
    return df
