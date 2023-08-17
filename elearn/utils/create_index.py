import os
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ListIndex, SimpleWebPageReader, QuestionAnswerPrompt
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
dest_dir = []

source_dir = ['https://testdriven.io/blog/django-custom-user-model/']


def standard_reader(source_dir, dest_dir):
    reader = SimpleDirectoryReader(input_files=source_dir)
    documents = reader.load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=dest_dir)
    query_engine = index.as_query_engine()
    return query_engine

documents = SimpleWebPageReader(html_to_text=True).load_data(source_dir)
index = ListIndex.from_documents(documents)
query_str = 'Describe the custom user model'
QA_PROMPT_TMPL = (
        "Hello, I have some context information for you:\n"
        "---------------------\n"
        "{context_str}"
        "\n---------------------\n"
        "Based on this context, could you please help me understand the answer to this question: {query_str}?\n"
        )
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
query_engine = index.as_query_engine(text_qa_template=QA_PROMPT,)
answer = query_engine.query(query_str)
print(answer)


'''
# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context)
'''