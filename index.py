import os
import openai
from dotenv import load_dotenv
from llama_index import SimpleWebPageReader, StorageContext, SimpleDirectoryReader, load_index_from_storage, download_loader, VectorStoreIndex, QuestionAnswerPrompt
from llama_index.prompts.default_prompts import (DEFAULT_TEXT_QA_PROMPT_TMPL)

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')
# documents = SimpleDirectoryReader('data').load_data()

""" storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context) """
"""SimpleWebPageReader = download_loader("SimpleWebPageReader")
loader = SimpleWebPageReader()
documents = loader.load_data(urls=['https://testdriven.io/blog/django-custom-user-model/'])
index = VectorStoreIndex.from_documents(documents)
"""
print(openai.api_key)
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("What did the author do growing up?")
print(response)

