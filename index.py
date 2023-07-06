import openai
from extvar import *
from llama_index import SimpleDirectoryReader, QuestionAnswerPrompt, StorageContext, load_index_from_storage
from llama_index.storage.index_store import SimpleIndexStore
openai.api_key= OPENAI_API_KEY

storage_context = StorageContext.from_defaults(
  
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="index"),
)
index = load_index_from_storage(storage_context)
print('yay!')
query_engine = index.as_query_engine()
response1 = query_engine.query("What's the candidate's name?")
print(response1)
