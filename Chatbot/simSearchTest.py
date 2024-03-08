import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json


def search_for_relevant_datasets(user_query):
    # Load variables from .env file into environment
    load_dotenv()

    url = os.getenv("WOBBY_URL_ENDPOINT")

    querystring = {"limit": "10", "offset": "0", "sortBy": "relevance"}

    payload = {
        "query": user_query,
        "providers": [os.getenv("WOBBY_DATA_PROVIDER")]
    }

    headers = {
        "auth-token": os.getenv("WOBBY_API_AUTH_TOKEN"),
        "content-type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

    # Parse JSON text into a Python dictionary
    response_dict = json.loads(response.text)

    # Extract datasets from the dictionary
    datasets = response_dict.get('datasets', [])

    # Convert datasets into a DataFrame
    df = pd.json_normalize(datasets, max_level=1)

    return df[['dataset.id', 'dataset.shortDescription']].rename(
        columns={'dataset.id': 'id', 'dataset.shortDescription': 'description'})
