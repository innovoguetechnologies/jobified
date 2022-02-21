from django.db import models
from django.conf import settings
from candidate.models import Candidate
from company.models import Poc

class Client(models.Model):
	name = models.CharField(
		verbose_name = "Name of the company",
		max_length = 100,
		help_text = "Name of the company",
		blank = False,
	)
	address = models.TextField(
		verbose_name = "Address",
		help_text = "The address of the company, as in bank and official records",
		blank = False,
	)
	company_size_choices = [
		('SM' , 'Less than 20'),
		('MD' , '20 - 50'),
		('LG' , '50 - 250'),
		('XL' , '250+'),
	]
	company_size = models.CharField(
		verbose_name = "No of Employees",
		max_length = 3,
		choices = company_size_choices,
		help_text ="No of companies employees",
		blank = False,
		default = 'MD',
	)
	about = models.TextField(
		verbose_name = "About the company",
		help_text = "Describe your company",
		blank = False,
	)
	logo = models.ImageField(
		verbose_name = "Company Logo",
		upload_to = "client_logos/",
		blank = True
	)
	poc = models.ForeignKey(
		Poc,
		on_delete = models.CASCADE,
		editable = False,
		null = True,
	)

class Employee(models.Model):
	first_name = models.CharField(
		verbose_name = "First Name",
		max_length = 100,
		help_text = "First Name",
		blank = False,
	)
	last_name = models.CharField(
		verbose_name = "Last Name",
		max_length = 100,
		help_text = "Last Name",
		blank = True,
	)
	email = models.EmailField(
		verbose_name = "Email",
		help_text = "Email id of the candidate.",
		unique = True,
	)
	designation = models.CharField(
		verbose_name = "Designation",
		max_length = 30,
		blank = False,
	)
	profile_photo = models.ImageField(
		verbose_name = "Profile Photo",
		upload_to = "profile_photos/client/",
		blank = True
	)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE,
		editable = False
	)
	company = models.ForeignKey(Client, on_delete = models.CASCADE, editable = False)

class Job(models.Model):
	title = models.CharField(
		verbose_name = "Job Title",
		help_text = "Title of the job",
		max_length = 40,
		blank = False,
	)
	location = models.CharField(
		help_text = "Location of the job",
		max_length = 70,
		blank = False,
	)
	region = models.CharField(
		help_text = "Region of the job",
		max_length = 70,
		blank = False,
	)
	job_types = [
		('Full Time', 'Full Time'),
		('Internship', 'Internship'),
		('Part Time', 'Part Time'),
		('Temporary', 'Temporary'),
	]
	job_type = models.CharField(
		choices = job_types,
		max_length = 10,
		blank = False,
		help_text = "Type of the vaccancy",
		default = 'Full'
	)
	category = models.CharField(
		max_length = 30,
		blank = False,
		help_text = "Category of the job",
	)
	tags = models.CharField(
		max_length = 255,
		blank = False,
		help_text = "Tags which best describes the job."
	)
	description = models.TextField(
		help_text = "Description of the job",
		blank = False,
	)
	salary = models.IntegerField(
		help_text = "Salary for the job",
		blank = False,
	)
	added = models.DateField(
		auto_now_add = True,
		help_text = "Date of adding this job",
	)
	client = models.ForeignKey(Client, on_delete = models.CASCADE, editable = False)
	applicants = models.ManyToManyField(
		Candidate,
		related_name = 'jobs',
		through = 'Schedule',
		through_fields = ('job', 'candidate'),
		editable = False,
	)

class Schedule(models.Model):
	screening_statuses = [
		('Not Screened', 'Not Screened'),
		('Passed', 'Passed'),
		('Failed', 'Failed'),
	]
	screening_status = models.CharField(
		max_length = 12,
		choices = screening_statuses,
		verbose_name = "Screening Status",
		default = "Not Screened",
	)
	interview_date = models.DateTimeField(
		verbose_name = "Time of the interview",
		null = True,
		blank = True
	)
	interview_statuses = [
		('Not Done', 'Not Done'),
		('Accepted', 'Accepted'),
		('Rejected', 'Rejected'),
	]
	interview_status =models.CharField(
		max_length = 8,
		choices = interview_statuses,
		verbose_name = "Interview Status",
		default = "Not Done",
	)
	date_joined = models.DateField(
		verbose_name = "Date of Joining",
		null = True,
		blank = True,
	)
	progress = models.IntegerField(
		default = 0,
		verbose_name = "Progress of the schedule",
	)
	candidate = models.ForeignKey(
		Candidate,
		on_delete = models.CASCADE,
		editable = False
	)
	job = models.ForeignKey(
		Job,
		on_delete = models.CASCADE,
		editable = False
	)
