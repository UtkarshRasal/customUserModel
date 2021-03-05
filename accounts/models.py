from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
#import uuid 

class UserManager(BaseUserManager):
	def create_user(self, username, email, password=None):

		if username is None:
			raise TypeError('User should have a username')

		if email is None:
			raise TypeError('User should have a email')

		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save()		
		return user		

	def create_superuser(self, username, email, password=None):

		if password is None:
			raise TypeError('Password should not be None')

		if email is None:
			raise TypeError('Email should not be None')

		user = self.create_user(username, email, password)	
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

class User(AbstractBaseUser, PermissionsMixin):
	#uid = models.UUIDField(default=uuid.uuid4)
	username = models.CharField(max_length=255, unique=True, db_index=True)
	email = models.EmailField(max_length=255, unique=True, db_index=True)
	is_verified = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIEDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def tokens(self):
		return ''

	



