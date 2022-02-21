from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	path('', views.accountrootView, name = 'AccountRoot'),
	path('login/<str:usertype>/', views.loginView, name = 'login'),
	path('logout/', views.logoutView, name = 'logout'),
	path('register/candidate/', views.candidateRegisterView, name = 'register_candidate'),
	path('register/consultant/', views.consultantRegisterView, name = 'register_consultant'),
	path('register/client/', views.clientRegisterView, name = 'register_client'),
	path('success/', views.successView, name = 'success'),
	path('password/', views.changePasswordView, name = 'change_password'),
	path('send_otp/', views.sendOTPView, name = 'send_otp'),
]
 
