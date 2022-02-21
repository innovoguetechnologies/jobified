# Company dashboard views

# Built-in imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.contrib.auth.models import Group


import random
from string import ascii_letters, digits

# Custom imports
from .decorators import company_required
from .forms import RegPocForm
from accounts.forms import AddSubordinateForm
from accounts.models import User
from client.models import Client, Job, Schedule
from candidate.models import Candidate
from company.models import Poc

@login_required
@company_required
def dashboardView(request):
	clients = Client.objects.filter(poc = request.user.poc)
	context = {
		'clients' : clients,
	}
	return render(request, 'company/dashboard.html', context = context)

@login_required
@company_required
def listNewClientsView(request):
	clients = Client.objects.filter(poc = None)
	context = {
		'clients' : clients,
	}
	return render(request, 'company/new/list.html', context = context)

@login_required
@company_required
def becomePOCView(request, client_id):
	client = Client.objects.get(pk = client_id)
	if client.poc is None:
		client.poc = request.user.poc
		client.save()
		messages.success(request, "Succesfully added you as the company's POC.")
		return redirect('company_dashboard')
	else:
		messages.error(request, "Somebody else became their POC first")
		return redirect('list_new_clients')

@login_required
@company_required
def viewClientView(request, client_id):
	client = Client.objects.get(pk = client_id)
	jobs = Job.objects.filter(client = client_id)
	context = {
		'client' : client,
		'jobs' : jobs,
	}
	return render(request, 'company/existing/view_client.html', context = context)

@login_required
@company_required
def listApplicantsView(request, job_id):
	# Getting all applicants for the given job_id
	candidates = Candidate.objects.filter(jobs = job_id)
	context = {
		'candidates' : candidates,
		'job_id' : job_id,
	}
	return render(request, 'company/existing/applicants/list.html', context = context)

@login_required
@company_required
def viewApplicantView(request, job_id, candidate_id):
	schedule = Schedule.objects.get(job = job_id, candidate = candidate_id)
	schedule.candidate.skills = schedule.candidate.skills.strip('][').split(',')
	schedule.candidate.languages = schedule.candidate.languages.strip('][').split(',')
	schedule.candidate.certifications = schedule.candidate.certifications.strip('][').split(',')
	context = {
		'schedule' : schedule,
	}
	return render(request, 'company/existing/applicants/view.html', context = context)

@login_required
@company_required
@user_passes_test(lambda u: u.is_superuser, login_url = 'home')
def adminView(request):
	client_count = Client.objects.all().count()
	job_count = Job.objects.all().count()
	joined_count = Schedule.objects.all().count()
	candidate_count = Candidate.objects.all().count()
	pocs = Poc.objects.all()
	context = {
		'client_count' : client_count,
		'job_count' : job_count,
		'candidate_count' : candidate_count,
		'joined_count' : joined_count,
		'pocs' : pocs,
	}
	return render(request, 'company/admin/summary.html', context = context)

@login_required
@company_required
@user_passes_test(lambda u: u.is_superuser, login_url = 'home')
def addPocView(request):
	# Form to add new member
	data = dict()
	if request.method == 'POST' and request.is_ajax():
		print("inside save function")
		auth_details = AddSubordinateForm(request.POST)
		poc_details = RegPocForm(request.POST)
		# Creating a random password
		random_password = ''.join((random.choice(ascii_letters + digits) for i in range(9)))
		if (auth_details.is_valid() and poc_details.is_valid()):
			print("Forms are valid")
			phone_no = auth_details.cleaned_data['phone_no']
			print(random_password)
			poc = poc_details.save(commit = False)
			# Create a user with random password and link to consultant
			user = User.objects.create_user(phone_no = phone_no, password = random_password)
			user.save()
			company_group, created = Group.objects.get_or_create(name = 'company')
			user.groups.add(company_group)
			
			poc.user = user
			poc.save() # Save the poc
			data['form_is_valid'] = True
			#Updating the members list
			pocs = Poc.objects.all()
			data['html_member_list'] = render_to_string('company/admin/_list.html', {
				'pocs': pocs,
			})
		else:
			data['form_is_valid'] = False
	else:
		auth_details = AddSubordinateForm()
		poc_details = RegPocForm()
		context = {
			'auth_details_form' : auth_details,
			'poc_details_form' : poc_details,
		}
		data['html_form'] = render_to_string('company/admin/add.html', context, request = request)
	return JsonResponse(data)
