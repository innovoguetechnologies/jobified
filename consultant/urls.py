# Consultant app url configurations

# Django built-in features imports
from django.conf.urls import url
from django.urls import path

# Userdefined features imports
from . import views

urlpatterns = [
	path('', views.dashboardView, name = 'consultant_dashboard'),
	path('members/add/', views.addMemberView, name = 'add_member'),
	path('members/list/', views.listMembersView, name = 'list_members')
]
