from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.authtoken.models import Token

from .managers import CustomUserManager

# Create your models here.

'''def get_default_profile_image():
	return 'account/nnajidanny004@gmail.com/20221119_205632.jpg'

def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png' '''

class Account(AbstractBaseUser, PermissionsMixin):
	email 					= models.EmailField(verbose_name="email", max_length=30, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	#first_name				= models.CharField(max_length=30, null=True, blank=True)
	#last_name 				= models.CharField(max_length=30, null=True, blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	#profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	#hide_email				= models.BooleanField(default=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['username', ]

	objects = CustomUserManager()

	def __str__(self):
		return self.email
	
	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
	
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
	
'''def upload_location(instance, filename):
    file_path = 'account/{profile_id}/{filename}'.format(
        profile_id=str(instance.user), filename=filename
    )
    return file_path'''


	    
