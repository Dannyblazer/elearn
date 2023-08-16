
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None, is_student=False, is_instructor=False):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have an username")

		user  = self.model(
				email=self.normalize_email(email),
				username=username,
				is_instructor=is_instructor,
            	is_student=is_student
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user  = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
			)
		user.is_instructor = True
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	bio 					= models.TextField(max_length=250, blank=True)
	is_student 				= models.BooleanField(default=False)
	is_instructor			= models.BooleanField(default=False)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	# first_name 				= models.CharField(max_length=30)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username',]

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True
	
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)
	

def upload_location(instance, filename):
    file_path = 'account/{profile_id}/{filename}'.format(
        profile_id=str(instance.account), filename=filename
    )
    return file_path

