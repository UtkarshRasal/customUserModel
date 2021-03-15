from rest_framework import serializers
from .models import User
import uuid

class RegisterSerializer(serializers.ModelSerializer):
	uid = serializers.UUIDField(required=False)
	password = serializers.CharField(max_length=60, min_length=8, write_only=True)

	class Meta:
		model = User
		fields = ['uid', 'email', 'password']

	def validate(self, attrs):
		email = attrs.get('email', '')
		# username = attrs.get('username', '')

		# if not username.isalnum():
		# 	raise serializers.ValidationError('The username should only contain alphanumeric characters')
		return attrs

class LoginSerializer(serializers.ModelSerializer):
	# email = serializers.EmailField(max_length=255)
	# password = serializers.CharField(max_length=60, min_length=8, write_only=True)

	class Meta:
		model = User
		fields = ['email', 'password']

class ForgotPasswordSerializer(serializers.ModelSerializer):
	uid = serializers.UUIDField(required=False)

	class Meta:
		model = User
		fields = ['uid','email']
	
class ChangePasswordSerializer(serializers.ModelSerializer):
	confirm_password = serializers.CharField(max_length=60, min_length=8, write_only=True)

	class Meta:
		model = User
		fields = ['password', 'confirm_password']

	


