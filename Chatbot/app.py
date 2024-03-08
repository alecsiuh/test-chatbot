import os
from OpenAi.openai_client import OpenAIClient
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def main():
    # Load environment variables from .env
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")

    # Check if the API key is available
    if api_key is None:
        raise ValueError("API key not found. Make sure you have set OPENAI_API_KEY in your environment.")

    # Initialize the OpenAI client
    openai_client = OpenAIClient(api_key)

    while True:

        #give me insights on dataset 11540f13-16d8-44a9-b560-fa682eadc834
        user_query = input("Enter your question: ")
        if user_query.lower() == 'exit':
            break

        gpt_response = openai_client.get_gpt3_response(user_query)
        print("GPT-3 Response:", gpt_response)


if __name__ == "__main__":
    main()
