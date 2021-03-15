from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import (RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ChangePasswordSerializer)
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site 
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import ListCreateAPIView



class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request):
		global user_uuid
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		user_data = serializer.data
		user_uuid = user_data['uid']
		print('userId', user_uuid)
		user = User.objects.get(email=user_data['email'])

		token = RefreshToken.for_user(user).access_token
		current_site = get_current_site(request).domain
		relativeLink = "/auth/email-verify/"
		absurl = 'http://'+ current_site + relativeLink + user_uuid 

		email_body = 'Hi user use link below to verify your email \n' + absurl 
		data = {'email_body': email_body,'to_email': user.email, 'email_subject':'Verify Your Email'}

		Util.send_email(data)

		return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
	def get(self, request, pk):
		token = request.GET.get('token')
		print(pk)
		try:
			user = User.objects.get(uid = pk)
			if user:
				user.is_verified = True
				user.save()
			return Response({'email':'Succesfully activated'}, status=status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({'Not a valid token'}, status=status.HTTP_400_BAD_REQUEST)
		

class LoginView(generics.GenericAPIView):
	serializer_class = LoginSerializer
	def post(self, request):
		
		user = self.request.data
		
		try:
			for field in ['email', 'password']:
				if not user.get(field):
					raise Response(f"{field} is required", status=status.HTTP_400_BAD_REQUEST)
			email = self.request.data['email']
			password = self.request.data['password']
			
			_user = User.objects.get(email=email)


			if not _user.is_verified:
				return Response(f"User not Verified", status=status.HTTP_400_BAD_REQUEST)

			if _user.password != password:
				return Response(f"Incorrect Password", status=status.HTTP_400_BAD_REQUEST)
			print('view 2')
			token = RefreshToken.for_user(_user)
			serializer_class = LoginSerializer(_user)
			_data = serializer_class.data
			return Response({
				'message':'Login Successful',
				'access': str(token.access_token)
				})
		except User.DoesNotExist:
			print('ERROR')
			return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(generics.GenericAPIView):
	serializer_class = ForgotPasswordSerializer
	def post(self, request):
		user = self.request.data
		import pdb
		pdb.set_trace()
		try:
			if not user.get('email'):
				return Response(f"Enter your correct email", status=status.HTTP_400_BAD_REQUEST)
			
			
			email = self.request.data['email']
			_user = User.objects.get(email=email)


			serializer_class = ForgotPasswordSerializer(_user)
			_data = serializer_class.data
			relativeLink = "/auth/change-pass/"
			current_site = get_current_site(request).domain
			absurl = 'http://'+ current_site + relativeLink + str(_user.uid) 

			email_body = 'Hi user, use this link to change your password \n' + absurl 
			data = {'email_body': email_body,'to_email': _user.email, 'email_subject':'Change your password'}

			Util.send_email(data)

			return Response(_data, status=status.HTTP_201_CREATED)
		except User.DoesNotExist:
			print('ERROR')
			return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(generics.GenericAPIView):
	serializer_class = ChangePasswordSerializer
	def post(self, request, pk):
		try:
			user = self.request.data
		
			for field in ['password', 'confirm_password']:
				if not user.get(field):
					raise Response(f"{field} cannot be empty", status=status.HTTP_400_BAD_REQUEST)
				
			if user['password'] != user['confirm_password'] :
				return Response(f"Password doesn't match", status=status.HTTP_400_BAD_REQUEST)

			_user = User.objects.get(uid=pk)
			_user.set_password(user['password'])
			_user.save()
			
			return Response(f"Password changed Succesfully", status.HTTP_201_CREATED)

		except User.DoesNotExist:
			print('ERROR')
			return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)	
			

class UserListing(ListCreateAPIView):
	"""docstring for UserListing"""
	serializer_class = LoginSerializer
	queryset = User.objects.all()
	permission_classes = [permissions.IsAuthenticated]