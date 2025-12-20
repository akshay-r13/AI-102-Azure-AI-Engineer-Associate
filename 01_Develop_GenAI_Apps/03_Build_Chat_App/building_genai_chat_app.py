import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv('.env')

project = AIProjectClient(
    endpoint=os.environ['FOUNDRY_PROJECT_ENDPOINT'],
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credentual=True
    )
)

openai_client = project.get_openai_client(api_version="2024-10-21")

prompt = [
    {
        "role": "system",
        "content": "You are a history teacher"
    }
]

while (True):
    input_text = input()
    if input_text == "quit":
        break
    prompt.append({"role": "user", "content": input_text})
    response = openai_client.chat.completions.create(messages = prompt, model = "gpt-4o")
    print(response.choices[0].message.content)
