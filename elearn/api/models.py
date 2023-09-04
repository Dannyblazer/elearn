from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from llama_index import VectorStoreIndex
from users.models import Account  # Import the Account model from your accounts app

def get_upload_filename(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.uploader.id, filename)

class Uploads(models.Model):
    uploader = models.ForeignKey(Account, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_filename)

    def __str__(self):
        return str(self.file)

@receiver(post_save, sender=Uploads)
def indexer(sender, instance, created, **kwargs):
    if created:
        index = VectorStoreIndex.from_documents(instance)
        index.storage_context.persist(persist_dir=upload_location)

def upload_location(instance, filename):
    file_path = 'indexed/{profile_id}/{filename}'.format(
        profile_id=str(instance.uploader.id), filename=filename
    )
    return file_path
