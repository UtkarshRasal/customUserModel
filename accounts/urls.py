from django.urls import path
from .views import (RegisterView, 
					VerifyEmail, 
					LoginView,
					ForgotPasswordView,
					ChangePasswordView,
					UserListing,
				)			

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginView.as_view(), name='login'),
	path('email-verify/<str:pk>/', VerifyEmail.as_view(), name='email-verify'),
	path('forgotPass/', ForgotPasswordView.as_view(), name='forgotPass'),
	path('change-pass/<str:pk>/', ChangePasswordView.as_view(), name='change-pass'),
	path("users/", UserListing.as_view()),
]