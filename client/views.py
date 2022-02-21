# Consultant's WebView Configurations

# Built-in feature import
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import Group

import random
from string import ascii_letters, digits
import datetime

# User defined feature import
from .models import Client, Employee, Job, Schedule
from .forms import RegEmployeeForm, AddJobForm, ApplicantStatusForm, SearchForm, EmployeeInfoForm, ClientInfoForm
from accounts.forms import AddSubordinateForm
from .decorators import client_required, boss_required
from accounts.models import User
from candidate.models import Candidate

def is_client(user):
	return user.groups.filter(name='client').exists()

@login_required
@client_required
def addEmployeeView(request):
	# Form to add new member
	data = dict()
	if request.method == 'POST' and request.is_ajax():
		print("inside save function")
		auth_details = AddSubordinateForm(request.POST)
		employee_details = RegEmployeeForm(request.POST)
		# Creating a random password
		random_password = ''.join((random.choice(ascii_letters + digits) for i in range(9)))
		if (auth_details.is_valid() and employee_details.is_valid()):
			print("Forms are valid")
			phone_no = auth_details.cleaned_data['phone_no']
			print(random_password)
			employee = employee_details.save(commit = False)
			# Create a user with random password and link to consultant
			user = User.objects.create_user(phone_no = phone_no, password = random_password)
			client_group, created = Group.objects.get_or_create(name = 'client')
			user.groups.add(client_group)
			
			employee.user = user
			employee.company = request.user.employee.company # Link the firm of the boss to consultant
			employee.save() # Save the employee
			data['form_is_valid'] = True
			#Updating the members list
			employees = Employee.objects.filter(company = request.user.employee.company)
			data['html_member_list'] = render_to_string('client/employees/_list.html', {
				'employees': employees,
			})
		else:
			data['form_is_valid'] = False
	else:
		auth_details = AddSubordinateForm()
		employee_details = RegEmployeeForm()
		context = {
			'auth_details_form' : auth_details,
			'employee_details_form' : employee_details,
		}
		data['html_form'] = render_to_string('client/employees/add.html', context, request = request)
	return JsonResponse(data)

@login_required
@client_required
def listEmployeesView(request):
	# Returns the client companie's employees list and operations.
	employees = Employee.objects.filter(company = request.user.employee.company)
	context = {
		'employees' : employees,
	}
	return render(request, 'client/employees/list.html', context = context)

@login_required
@client_required
def listJobView(request):
	# Returns all the job's posted by the client company
	jobs = Job.objects.filter(client = request.user.employee.company)
	context = {
		'jobs' : jobs,
	}
	return render(request, 'client/jobs/list.html', context = context)

@login_required
@client_required
def addJobView(request):
	# Returns form to add new job
	data = dict()
	if request.method == 'POST' and request.is_ajax():
		print("inside save function")
		job_details = AddJobForm(request.POST)
		if (job_details.is_valid()):
			print("Forms are valid")
			job = job_details.save(commit = False)
			job.client = request.user.employee.company # Link the job to the user's company
			job.save() # Save the employee
			data['form_is_valid'] = True
			#Updating the Jobs list
			jobs = Job.objects.filter(client = request.user.employee.company)
			data['html_member_list'] = render_to_string('client/jobs/_list.html', {
				'jobs': jobs,
			})
		else:
			data['form_is_valid'] = False
	else:
		job_details_form = AddJobForm()
		context = {
			'job_details_form' : job_details_form,
		}
		data['html_form'] = render_to_string('client/jobs/add.html', context, request = request)
	return JsonResponse(data)

@login_required
@client_required
def dashboardView(request):
	# Getting all schedules for the client
	month = datetime.date.today() - datetime.timedelta(days = 120)
	schedules = Schedule.objects.filter(job__client = request.user.employee.company).filter(job__added__gt = month)
	#Counting schedules for each status
	new_count = schedules.filter(screening_status = "Not Screened").count()
	screened_count = schedules.filter(screening_status = "Passed").count()
	scheduled_count = schedules.filter(interview_date = None).count()
	interviewed_count = schedules.filter(interview_status = "Accepted").count()
	joined_count = schedules.filter(~Q(date_joined = None)).count()

	context = {
		'new_count' : new_count,
		'screened_count' : screened_count,
		'interviewed_count' : interviewed_count,
		'joined_count' : joined_count,
	}
	return render(request, 'client/dashboard.html', context = context)

@login_required
@client_required
def listApplicantView(request, job_id):
	# Getting all applicants for the given job_id
	candidates = Candidate.objects.filter(jobs = job_id)
	context = {
		'candidates' : candidates,
		'job_id' : job_id,
	}
	return render(request, 'client/applicants/list.html', context = context)

@login_required
@client_required
def updateScheduleView(request, schedule_id):
	#Getting the details of Schedule
	schedule = Schedule.objects.get(pk = schedule_id)
	print(request.method, " ", request.is_ajax())
	if request.method == 'POST' and request.is_ajax():
		schedule_form = ApplicantStatusForm(request.POST, instance = schedule);
		if schedule_form.is_valid():
			schedule_form.save()
		else:
			print("form invalid")
	else:
		schedule_form = ApplicantStatusForm(instance = schedule)
		print("not post or ajax")
	context = {
		'schedule':schedule,
		'schedule_form' : schedule_form,
	}
	data = {
		'html' : render_to_string('client/applicants/update_status.html', context = context, request = request)
	}
	return JsonResponse(data)

@login_required
@client_required
def viewApplicantView(request, job_id, candidate_id):
	schedule = Schedule.objects.get(job = job_id, candidate = candidate_id)
	schedule_form = ApplicantStatusForm(instance = schedule)
	schedule.candidate.skills = schedule.candidate.skills.strip('][').split(',')
	schedule.candidate.languages = schedule.candidate.languages.strip('][').split(',')
	schedule.candidate.certifications = schedule.candidate.certifications.strip('][').split(',')
	context = {
		'schedule' : schedule,
		'schedule_form' : schedule_form
	}
	return render(request, 'client/applicants/view.html', context = context)

@login_required
@client_required
def listEachScheduleStatusView(request, progress):
	schedules = Schedule.objects.filter(job__client = request.user.employee.company, progress = progress)
	if(progress == 0):
		title = "Status : New"
	elif(progress == 25):
		title = "Status : Screened"
	elif(progress == 50):
		title = "Status : Scheduled"
	elif(progress == 75):
		title = "Status : Interviewed"
	else:
		title = "Status : Joined"
	context = {
		'schedules' : schedules,
		'title' : title,
	}
	return render(request, 'client/dashboard/list.html', context = context)

@login_required
@client_required
def searchView(request):
	if request.method == 'POST':
		search_form = SearchForm(request.POST)
		if search_form.is_valid():
			entity = search_form.cleaned_data['search']
			client = request.user.employee.company
			jobs = Job.objects.filter(client = client, title__icontains = entity, )
			schedules = Schedule.objects.filter(
				Q(candidate__first_name__icontains = entity)|Q(candidate__last_name__icontains = entity)|Q(job__title__icontains = entity),
				job__client = client
			)
			context = {
				'jobs' : jobs,
				'schedules' : schedules,
			}
			return render(request, 'client/search_list.html', context = context)
	else:
		search_form = SearchForm()
		context = {
			'search_form' : search_form,
		}
		return render(request, 'client/nav/search.html', context = context)

@login_required(login_url='/accounts/login/client/')
@client_required
def profileUpdateView(request):
	employee = request.user.employee
	if(request.method == "POST"):
		profile_form = EmployeeInfoForm(request.POST, request.FILES, instance = employee)
		# Calculating Experience
		if(profile_form.is_valid()):
			print("Form is valid")
			p = profile_form.save()
		else:
			print("Form is not valid")
	else:
		profile_form = EmployeeInfoForm(instance = employee)
	context = {
		'profile_form' : profile_form,
	}
	return render(request, 'client/profile.html', context=context)
	
@login_required(login_url='/accounts/login/client/')
@boss_required
def clientProfileUpdateView(request):
	client = request.user.employee.company
	if(request.method == "POST"):
		client_info_form = ClientInfoForm(request.POST, request.FILES, instance = client)
		# Calculating Experience
		if(client_info_form.is_valid()):
			print("Form is valid")
			p = client_info_form.save()
		else:
			print("Form is not valid")
	else:
		client_info_form = ClientInfoForm(instance = client)
	context = {
		'client_info_form' : client_info_form,
	}
	return render(request, 'client/client_profile.html', context=context)
