import spacy

nlp = spacy.load("nl_core_news_md")


class SimilaritySearch:
    def get_most_similar_datasets(user_query, dataset_descriptions):
        user_query_doc = nlp(user_query)

        # Calculate similarity between the user query and each dataset description
        similarity_scores = []
        for description in dataset_descriptions:
            description_doc = nlp(description['description'])
            similarity_score = user_query_doc.similarity(description_doc)
            similarity_scores.append((description, similarity_score))

        # Sort
        sorted_descriptions = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Return the top 3 most similar dataset descriptions
        return sorted_descriptions[:3]

# Code that might help going forward

# Modify your get_gpt3_response function to use this new function
# def get_gpt3_response(message, dataset_descriptions):
#     # Existing code...
#
#     elif function_name == 'get_dataset_descriptions':
#         top_similar_datasets = get_most_similar_datasets(message, dataset_descriptions)
#         for dataset, similarity_score in top_similar_datasets:
#             messages.append({"role": "function", "name": "get_dataset_descriptions", "content": json.dumps(dataset)})
#         # Send the updated messages back to GPT-3 for a new response
#         response_with_function_result = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=messages
#         )
#         return response_with_function_result.choices[0].message.content
