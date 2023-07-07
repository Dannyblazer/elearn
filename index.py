import os
import openai
from dotenv import load_dotenv
from llama_index import StorageContext, SimpleDirectoryReader, load_index_from_storage

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')
documents = SimpleDirectoryReader('data').load_data()

storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()
address = query_engine.query("Where is the candidate's address and Name?")
print(address)
