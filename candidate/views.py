# Consultant's WebView Configurations

# Built-in feature import
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# User defined feature import
from client.models import Job, Schedule
from .forms import ProfileForm, FilterForm
from .decorators import candidate_required
from .models import Candidate

# View function for candidates Dashboard
@login_required(login_url='/accounts/login/candidate/')
@candidate_required
def dashboardView(request):
	c = request.user.candidate
	jobs = c.jobs.all()
	context = {
		'jobs' : jobs,
	}
	return render(request, 'candidate/dashboard.html', context = context)

# View function for updating the candidate profile
@login_required(login_url='/accounts/login/candidate/')
@candidate_required
def profileUpdateView(request):
	candidate = request.user.candidate
	if(request.method == "POST"):
		profile_form = ProfileForm(request.POST, request.FILES, instance = candidate)
		# Calculating Experience
		if(profile_form.is_valid()):
			print("Form is valid")
			exp = int(profile_form.cleaned_data['work_exp_year']) + (int(profile_form.cleaned_data['work_exp_month']) / 12)
			p = profile_form.save(commit=False)
			p.experience = exp
			p.save()
		else:
			print("Form is not valid")
	else:
		profile_form = ProfileForm(instance = candidate)
	context = {
		'profile_form' : profile_form,
	}
	return render(request, 'candidate/profile/update.html', context=context)

# View function for showing candidate's profile
def profileView(request):
	candidate = request.user.candidate
	candidate.skills = candidate.skills.strip('][').split(',')
	candidate.languages = candidate.languages.strip('][').split(',')
	candidate.certifications = candidate.certifications.strip('][').split(',')
	context = {
		'candidate' : candidate,
	}
	return render(request, 'candidate/profile/view.html', context = context)

# View function for listing all new jobs
def allJobsView(request):
	jobs = Job.objects.all()
	filter_form = FilterForm()
	if request.POST:
		filter_form = FilterForm(request.POST)
		if filter_form.is_valid():
			jobs = jobs.filter(
				Q(title__icontains = filter_form.cleaned_data['keyword'])|Q(client__name__icontains = filter_form.cleaned_data['keyword']),
				location__icontains = filter_form.cleaned_data['location'],
				job_type__exact = filter_form.cleaned_data['job_type']
			)
	context = {
		'jobs' : jobs,
		'filter_form' : filter_form,
	}
	return render(request, 'candidate/jobs/list.html', context = context)

@login_required(login_url='/accounts/login/candidate/')
@candidate_required
def viewJobView(request, job_id):
	data = dict()
	job = Job.objects.get(pk=job_id)
	context = {
		'job' : job,
	}
	data['job_desc'] = render_to_string('candidate/jobs/view.html', context)
	return JsonResponse(data)

@login_required(login_url='/accounts/login/candidate/')
@candidate_required
def applyJobView(request, job_id):
	data = dict()
	j = Job.objects.get(pk = job_id)
	j.applicants.add(request.user.candidate)
	data['message'] = '<div class="alert alert-success alert-dismissible fade show" role="alert"><span class="alert-icon"><i class="ni ni-like-2"></i></span><span class="alert-text">Applied Successfully</span><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
	return JsonResponse(data)

@login_required(login_url='/accounts/login/candidate/')
@candidate_required
def scheduleView(request, job_id):
	schedule = Schedule.objects.get(job = job_id, candidate = request.user.candidate)
	tags = schedule.job.tags.split(', ')
	context = {
		'schedule' : schedule,
		'tags' : tags,
	}
	return render(request, 'candidate/schedule/view.html', context = context)
