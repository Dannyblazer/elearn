from django.shortcuts import render
import os, openai
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, QuestionAnswerPrompt, download_loader, StorageContext, load_index_from_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
load_dotenv()
class AskView(View):
    def get(self, request, *args, **kwargs):
        query_str = request.GET.get('question', None)
        if not query_str:
            return JsonResponse({"error": "Please provide a question."}, status=400)
        
        # Load the index from disk
        openai.api_key = os.getenv('OPENAI_API_KEY')
        print(openai.api_key)
        index_file_path = os.path.join(settings.BASE_DIR, 'indexed_articles/django_custom_user_model', )
        storage_context = StorageContext.from_defaults(persist_dir=index_file_path)
        index = load_index_from_storage(storage_context)
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
        return JsonResponse({'answer': answer.response})
    def post(self, request, *args, **kwargs):
        # Handle POST requests if needed
        pass

