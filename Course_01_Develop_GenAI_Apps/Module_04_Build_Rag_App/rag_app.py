import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv('.env')


openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
search_url=os.getenv("AZURE_SEARCH_URL")
search_index_name='brochures-index'
search_key=os.getenv("AZURE_SEARCH_API_KEY")
embedding_model_name=os.getenv("EMBEDDING_MODEL") 
chat_model=os.getenv("CHAT_MODEL")

chat_client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key,
    api_version="2024-12-01-preview"
)

prompt = [
    {
        "role": "system",
        "content": "You are a travel assistant for Margie's travels and you provide information to users about travel services available"
    }
] # set the initial prompt

while True:
    user_input = input("Enter Response: (or type 'quit' to exit)")
    if user_input.strip().lower() == 'quit':
        break
    # add user input to prompt
    prompt.append({"role": "user", "content": user_input})
    # Set rag params
    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_url,
                    "index_name": search_index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_key
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": embedding_model_name
                    }
                }
            }
        ]
    }

    responses = chat_client.chat.completions.create(
        model=chat_model,
        messages=prompt,
        extra_body=rag_params
    )

    completion = responses.choices[0].message.content
    print(completion)

    prompt.append({"role": "assistant", "content": completion})