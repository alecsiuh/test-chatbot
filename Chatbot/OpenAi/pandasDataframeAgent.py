import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType

def process_dataframe_with_natural_language(df: pd.DataFrame, query):
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-0125"),
        df,
        verbose=False,
        return_intermediate_steps=True,
        agent_type=AgentType.OPENAI_FUNCTIONS
    ) 
    return agent.invoke(query)


# dataset = DatasetManager.get_datasets_by_dataset_id("11540f13-16d8-44a9-b560-fa682eadc834")
#
# agent2 = create_pandas_dataframe_agent(
#     ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-0125"),
#     dataset,
#     # verbose=True,
#     return_intermediate_steps=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS
# )
#
# while True:
#     user_input = input("Enter your query: ")  # Prompt the user for input
#     output = agent2.invoke(user_input)  # Invoke the agent with user input
#     # Extracting relevant information from the output dictionary
#     query = output['input']
#     result = output['output']
#     intermediate_steps = output['intermediate_steps']
#
#     # Printing the query
#     print("Query: ", query)
#
#     # Printing intermediate steps
#     print("\nIntermediate Steps:")
#     for step in intermediate_steps:
#         print(step)
#
#     # Printing the result
#     print("\nResult:")
#     print(result)
