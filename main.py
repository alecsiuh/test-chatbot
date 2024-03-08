import os
import json
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if api_key is None:
    raise ValueError("API key not found. Make sure you have set OPENAI_API_KEY in your environment.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

messages = [
    {"role": "system", "content": "if asked a data related question use the available datasets to answer the question"}
]

custom_functions = [
    {
        'name': 'get_dataset_descriptions',
        'description': 'Get the id and description of all the available local datasets'
    }]

def get_gpt3_response(message):
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=custom_functions,
        function_call="auto"
    )
    if response.choices[0].message.function_call:
        function_name = response.choices[0].message.function_call.name
        if function_name == 'get_dataset_descriptions':
            dataset_descriptions = get_dataset_descriptions()
            count = 0
            for dataset_description in dataset_descriptions:
                messages.append({"role": "function", "name": "get_dataset_descriptions", "content": json.dumps(dataset_description)})
                count+=1
                if count == 10:
                    break
            # Send the updated messages back to GPT-3 for a new response
            response_with_function_result = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response_with_function_result.choices[0].message.content
    elif response.choices[0].message.content is not None:
        content = response.choices[0].message.content
        messages.append({"role": "system", "content": content})
        return content
    else:
        return response


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


def get_dataset_descriptions():
    print("get_dataset_descriptions was called")
    datasets_descriptions = []
    for root, dirs, files in os.walk("./Chatbot/datasets"):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                with open(json_file_path, 'r') as f:
                    dataset_info = json.load(f)
                    dataset_id = dataset_info.get('dataset')
                    description = dataset_info.get('description')
                    if dataset_id and description:
                        datasets_descriptions.append({'dataset_id': dataset_id, 'description': description})
    return datasets_descriptions

def fetch_data_from_external_api():
    pass


def format_data(data):
    pass


if __name__ == "__main__":
    dataset = read_datasets('./Chatbot/datasets')

    while True:

        # print(get_dataset_descriptions())

        user_query = input("Enter your question: ")
        if user_query.lower() == 'exit':
            break

        gpt_response = get_gpt3_response(user_query)
        print("GPT-3 Response:", gpt_response)

