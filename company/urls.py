# Company app url configurations

# Django built-in features imports
from django.conf.urls import url
from django.urls import path

# Userdefined features imports
from . import views

urlpatterns = [
	path('', views.dashboardView, name = 'company_dashboard'),
	path('new/list/', views.listNewClientsView, name = 'list_new_clients'),
	path('new/apply/<int:client_id>/', views.becomePOCView, name = 'become_poc'),
	path('view/client/<int:client_id>/', views.viewClientView, name = 'view_client'),
	path('list/applicants/<int:job_id>', views.listApplicantsView, name = 'applicants_list'),
	path('view/applicant/<int:job_id>/<int:candidate_id>/', views.viewApplicantView, name = 'applicant_view'),
	path('admin/', views.adminView, name = 'admin'),
	path('poc/add/', views.addPocView, name = 'add_poc'),
]
