import os
from dotenv import load_dotenv
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.core.credentials import AzureKeyCredential

load_dotenv('.env')

azure_key_credential = AzureKeyCredential(key=os.getenv("COGNITIVE_SERVICES_KEY"))

qna_client = QuestionAnsweringClient(
    endpoint=os.getenv('COGNITIVE_SERVICES_ENDPOINT'),
    credential=azure_key_credential
)

qna_project_name=os.getenv("QNA_PROJECT_NAME")
qna_deployment_name=os.getenv("QNA_DEPLOYMENT_NAME")

# Submit a question and display the answer
user_question = ''
while True:
    user_question = input('\nQuestion:\n')
    if user_question.lower() == "quit":                
        break
    response = qna_client.get_answers(question=user_question,
                                    project_name=qna_project_name,
                                    deployment_name=qna_deployment_name)
    for candidate in response.answers:
        print(candidate.answer)
        print("Confidence: {}".format(candidate.confidence))
        print("Source: {}".format(candidate.source))