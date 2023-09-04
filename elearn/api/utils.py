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
SimpleWebPageReader = download_loader("SimpleWebPageReader")
loader = SimpleWebPageReader()
documents = loader.load_data(urls=['https://testdriven.io/blog/django-custom-user-model/'])
index = VectorStoreIndex.from_documents(documents)

QA_PROMPT_TMPL = (
    "Hello, I have some context information for you:\n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Based on this context, could you please help me understand the answer to this question: {query_str}?\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
query_engine = index.as_query_engine(text_qa_template=QA_PROMPT,)

query_str = "What are the advantages of using a custom User model in Django?"

response = query_engine.query(query_str)
print(response)
