# from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	path('', views.homeView, name="home"),
	path('home/', views.homeView, name="home"),
	path('about/', views.aboutView),
	path('dashboard/', views.dashboardView),
]
