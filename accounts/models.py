from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
#import uuid 

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):

		# if username is None:
		# 	raise TypeError('User should have a username')

		if email is None:
			raise TypeError('User should have a email')

		user = self.model(email=self.normalize_email(email))
		user.set_password(password)
		user.save()		
		return user		

	def create_superuser(self, email, password=None):

		if password is None:
			raise TypeError('Password should not be None')

		if email is None:
			raise TypeError('Email should not be None')

		user = self.create_user(email, password)	
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

class User(AbstractUser):
	#uid = models.UUIDField(default=uuid.uuid4)
	#username = models.CharField(max_length=255, unique=True, db_index=True)
	username = None
	email = models.EmailField(max_length=255, unique=True, db_index=True)
	is_verified = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = UserManager()
	def __str__(self):
		return self.email
