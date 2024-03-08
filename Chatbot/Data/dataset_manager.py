import os
import json
import pandas as pd
from dotenv import load_dotenv
import requests  

# Load variables from .env file into environment
load_dotenv()

class DatasetManager:
    @staticmethod
    def read_datasets(folder_path):
        datasets = {}
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                dataset_name = filename.split('.')[0]
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as json_file:
                    dataset_info = json.load(json_file)
                    datasets[dataset_name] = dataset_info
            elif filename.endswith('.parquet'):
                dataset_name = filename.split('.')[0]
                dataset_content = pd.read_parquet(os.path.join(folder_path, filename))
                datasets[dataset_name] = dataset_content
        return datasets

    @staticmethod
    def get_dataset_descriptions():
        # print("get_dataset_descriptions was called")
        dataset_catalogue = pd.DataFrame(columns=['id', 'description'])
        # for root, dirs, files in os.walk("./datasets"):
        for root, dirs, files in os.walk("./Chatbot/datasets"):
            for file in files:
                if file.endswith('.json'):
                    json_file_path = os.path.join(root, file)
                    with open(json_file_path, 'r') as f:
                        dataset_info = json.load(f)
                        dataset_id = dataset_info.get('dataset')
                        description = dataset_info.get('description')
                        if dataset_id and description:
                            dataset_catalogue.loc[len(dataset_catalogue)] = {'id': dataset_id,
                                                                             'description': description}
        return dataset_catalogue

    @staticmethod
    def search_for_relevant_datasets(user_query):
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

    @staticmethod
    def get_datasets_by_dataset_id(dataset_id):
        # print("get_datasets_by_dataset_id was called :", dataset_id)
        dataset = pd.DataFrame
        dataset_folder = f"./Chatbot/datasets/{dataset_id}"
        if os.path.exists(dataset_folder):
            for root, dirs, files in os.walk(dataset_folder):
                for file in files:
                    if file.endswith('.parquet'):
                        parquet_file_path = os.path.join(root, file)
                        # Read the parquet file into a pandas DataFrame
                        dataset = pd.read_parquet(parquet_file_path)
                        break
        else:
            print(f"Folder '{dataset_folder}' was not found")
        return dataset 

    @staticmethod
    def fetch_data_from_external_api():
        pass
