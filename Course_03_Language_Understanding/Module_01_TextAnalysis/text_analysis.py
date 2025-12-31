import os
from azure.ai.textanalytics import  TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv(".env")

key_credential = AzureKeyCredential(key=os.getenv("LANGUAGE_SERVICE_KEY"))

text_client = TextAnalyticsClient(
    endpoint=os.getenv("LANGUAGE_SERVICE_ENDPOINT"),
    credential=key_credential
)

reviews_folder_path = os.path.join('Course_03_Language_Understanding','Module_01_TextAnalysis','reviews')

docs = []

for file_ in os.listdir(reviews_folder_path):
    with open(os.path.join(reviews_folder_path, file_)) as f:
        file_content = f.read()
        docs.append(file_content)

language_detection_results = text_client.detect_language(documents=docs)
sentiment_analysis_results = text_client.analyze_sentiment(documents=docs)
key_phrases = text_client.extract_key_phrases(documents=docs)
named_entities = text_client.recognize_entities(documents=docs)
linked_entities = text_client.recognize_linked_entities(documents=docs)

for i in range(len(docs)):
    print("Review: ", docs[i])
    print("Primary Language: ", language_detection_results[i].primary_language)
    print("Key Phrases: ", key_phrases[i].key_phrases)
    print("Named Entities: ", {e.text: e.category for e in named_entities[i].entities})
    print("Linked Entities: ", {e.name: e.url for e in linked_entities[i].entities})
    print("Overall Sentiment: ", sentiment_analysis_results[i].sentiment)
    print("Sentence-wise Sentiment: ")
    for sentence in sentiment_analysis_results[i].sentences:
        print("\t", sentence.text, sentence.sentiment, sentence.confidence_scores)
    print("-" * 50)
    print()

