# Client app url configurations

# Django built-in features imports
from django.conf.urls import url
from django.urls import path

# Userdefined features imports
from . import views

urlpatterns = [
	path('', views.dashboardView, name = 'client_dashboard'),
	path('search/', views.searchView, name = 'search'),
	path('employees/add/', views.addEmployeeView, name = 'add_employee'),
	path('employess/list/', views.listEmployeesView, name = 'list_employees'),
	path('job/list/', views.listJobView, name = 'list_job'),
	path('job/add/', views.addJobView, name = 'add_job'),
	path('applicants/list/<int:job_id>', views.listApplicantView, name = 'list_applicants'),
	path('applicants/update/<int:schedule_id>/', views.updateScheduleView, name = 'update_schedule'),
	path('applicants/view/<int:job_id>/<int:candidate_id>/', views.viewApplicantView, name = 'view_applicant'),
	path('list/<int:progress>/', views.listEachScheduleStatusView, name = 'statuswise_list'),
	path('profile/', views.profileUpdateView, name = 'update_employee_profile'),
	path('profile/client/', views.clientProfileUpdateView, name = 'update_client_profile'),
]
