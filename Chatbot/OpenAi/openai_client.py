import json
from openai import OpenAI

from Data.dataset_manager import DatasetManager
from OpenAi.pandasDataframeAgent import process_dataframe_with_natural_language

# {
#     'name': 'get_datasets_by_dataset_id',
#     'description': 'Retrieve wanted datasets by their ids and get a list of pandas dataframes',
#     'parameters': {
#         'type': 'object',
#         'properties': {
#             'dataset_ids': {
#                 'type': 'array',
#                 'description': 'The ids of the datasets to retrieve',
#                 'items': {
#                     'type': 'string'
#                 }
#             }
#         }
#     }
# },

class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.messages = [
            {"role": "system",
             "content": "You are a helpful assistant that helps users with no experience with data analytics "
                        "process datasets and find patterns, insights and other data they might be looking for."},
            {"role": "system",
             "content": "If asked a data related question look into the available datasets or into a specific dataset "
                        "if provided an id and explain to the user why a certain dataset or more could be used to "
                        "answer their questions or queries."},
            {"role": "system",
             "content": "Most of the datasets are in Dutch rather than English so be careful not to make mistakes "
                        "when translating them and make sure the values and column names in dutch are used correctly."},
            {"role": "system",
             "content": "When calling a function make sure you provide all the needed arguments and that you retain "
                        "their outputs"},
            {"role": "system",
             "content": "When users ask for visualizations, guide them in selecting the right type of data "
                        "visualization based on their data and the insights they are aiming for. Different "
                        "visualizations serve different purposes, such as identifying trends, comparing groups, "
                        "or understanding distributions."},
            {
                "role": "system",
                "content": "When users ask for visualizations make sure that you are creating a chart that is interactive, "
                            "so that users can explore the data and gain insights from it. Interactive visualizations "
                            "allow users to filter, zoom, and hover over data points to see more details."
            },
            {"role": "system",
             "content": "Encourage users to enhance their visualizations with clear titles, axis labels, and legends "
                        "to make them easier to understand and more informative for the audience."},
            {"role": "system",
             "content": "Provide functionalities for displaying datasets directly to users, enabling them to view and interact "
                        "with their data in real-time. This includes presenting data tables, summaries, and basic visualizations "
                        "to give users an immediate sense of their dataset's structure and content."
            }
        ]

        self.custom_functions = [
            {
                'name': 'get_dataset_descriptions',
                'description': 'Get the id and description of all the available local datasets. This can be used when'
                               ' the user is vague or does not know what he is looking for. It can also be used to '
                               'lookup a dataset by its id.'
            },
            {
                'name': 'search_for_relevant_datasets',
                'description': 'When the user is looking for datasets about a specified topic or is looking for '
                               'something specific, this method return datasets that align what the user asks for.'
                               'Based on the users query, search through all the datasets and fetch the ones that'
                               ' best aligns with what the user wants. When fetching datasets you will receive the '
                               'dataset ids and description.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'user_query': {
                            'type': 'string',
                            'description': 'The user query made that holds the topic or context he is looking for.'
                        }
                    }
                }
            },
            {
                'name': 'process_dataframe_with_natural_language',
                'description': 'Process one or more datasets with natural language queries, you need to pass the wanted'
                               ' datasets id and the query made in natural language. Make sure you pass the dataset id '
                               'and query otherwise the function will not work. Use this method when asked to do '
                               'somthing with a specific dataset.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'dataframe_id': {
                            'type': 'string',
                            'description': 'The id of the dataset to be used to answer the query in natural language'
                        },
                        'query': {
                            'type': 'string',
                            'description': 'The natural language query or question asked about the datasets'
                        }
                    }
                }
            },
            {
                'name': 'show_dataset_object',
                'description': 'Return a dataset object to be displayed when the users uses the words "print" or "show" in prompt.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'dataset_id': {
                            'type': 'string',
                            'description': 'The id of the dataset to be shown or displayed'
                        }
                    }
                }
            }
        ]

    def get_gpt3_response(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            functions=self.custom_functions,
            function_call="auto"
        )
        if response.choices[0].message.function_call:
            function_name = response.choices[0].message.function_call.name
            print("function call: ", function_name)
            if function_name == 'get_dataset_descriptions':

                dataset_catalogue = DatasetManager.get_dataset_descriptions()
                print(dataset_catalogue)
                result = process_dataframe_with_natural_language(dataset_catalogue, "This is a dataset catalogue of "
                                                                                    "all the available datasets, it "
                                                                                    "holds 2 columns 'id' and "
                                                                                    "'description'. Note that the "
                                                                                    "datasets are un Dutch so when "
                                                                                    "searching for topics or terms, you"
                                                                                    " have to translate them to Dutch."
                                                                                    "When talking about a dataset, make"
                                                                                    " sure to extract and mention its "
                                                                                    "id. "
                                                                 + message)
                self.messages.append({"role": "system", "content": "Here is the result of the last dataset search :"
                                                                   + result['output'] + " This output is not displayed"
                                                                                        "to the user. Make sure to "
                                                                                        "explain the results and gide"
                                                                                        "the user through the process."
                                                                                        "Don't forget to explain Dutch"
                                                                                        " terms in English."
                                      })
                response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=self.messages
                )
                content = response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": content})
                return content

            elif function_name == 'search_for_relevant_datasets':
                # print(response)
                arguments = response.choices[0].message.function_call.arguments
                arguments_dict = json.loads(arguments)
                user_query = arguments_dict['user_query']
                relevant_datasets = DatasetManager.search_for_relevant_datasets(user_query)
                result = process_dataframe_with_natural_language(relevant_datasets, "These are the datasets that best "
                                                                                    "matches with what the user asked "
                                                                                    "for, look through them and pic "
                                                                                    "the ones that are best suited "
                                                                                    "based on the user query. The "
                                                                                    "dataset descriptions does not "
                                                                                    "mention what the datasets holds "
                                                                                    "exactly but return an estimation "
                                                                                    "of which ones would be most "
                                                                                    "useful. The dataset holds 2 "
                                                                                    "columns 'id' and 'description'. "
                                                                                    "When talking about a dataset, make"
                                                                                    " sure to mention its id. Here is "
                                                                                    "the user query :"
                                                                 + message)
                self.messages.append({"role": "system", "content": "Here is the result of the last dataset search :"
                                                                   + result['output'] + " This output is not displayed"
                                                                                        "to the user. Make sure to "
                                                                                        "explain the results and gide"
                                                                                        "the user through the process. Also when mentioning datasets "
                                                                                        "make sure to mension their ids."
                                      })
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=self.messages
                )
                content = response.choices[0].message.content
                self.messages.append({"role": "assistant", "content": content})
                return content

            elif function_name == 'process_dataframe_with_natural_language':

                # print("Agent wants to process dataframe(s) with natural language")

                # Extracting the 'arguments' field from the FunctionCall object
                arguments = response.choices[0].message.function_call.arguments

                # Parsing the JSON string to a Python dictionary
                arguments_dict = json.loads(arguments)
                print("response: ", response)
                print("arguments: ", arguments_dict)
                target_dataset = DatasetManager.get_datasets_by_dataset_id(arguments_dict['dataframe_id'])
                result = process_dataframe_with_natural_language(target_dataset, arguments_dict['query'])
                self.messages.append({"role": "assistant", "content": result['output']})
                return result['output'] 
            elif function_name == 'show_dataset_object':
                arguments = response.choices[0].message.function_call.arguments
                arguments_dict = json.loads(arguments)
                dataset_id = arguments_dict['dataset_id']
                self.messages.append({"role": "assistant", "content": "Here is the dataset"})
                return DatasetManager.get_datasets_by_dataset_id(dataset_id)
        elif response.choices[0].message.content is not None:
            content = response.choices[0].message.content
            self.messages.append({"role": "system", "content": content})
            return content
        else:
            return response
