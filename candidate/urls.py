# candidate app url configurations

from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
	path('', views.dashboardView, name = 'candidate_dashboard'),
	path('profile/', views.profileView, name = 'view_candidate_profile'),
	path('profile/update/', views.profileUpdateView, name = 'update_candidate_profile'),
	path('jobs/list/', views.allJobsView, name = 'list_vaccancies'),
	path('jobs/view/<int:job_id>', views.viewJobView, name = 'view_job'),
	path('jobs/apply/<int:job_id>', views.applyJobView, name = 'apply_job'),
	path('schedule/view/<int:job_id>/', views.scheduleView, name = 'candidate_schedule')
]
