import os
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, VectorStoreIndex, QuestionAnswerPrompt, download_loader
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')

SimpleDirectoryReader = download_loader("SimpleWebPageReader")

loader = SimpleDirectoryReader()
documents = loader.load_data(urls=['https://testdriven.io/blog/django-custom-user-model/'])
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="./indexed_articles/django_custom_user_model")

