from django.db import models
from django.conf import settings

from . import choices

class Candidate(models.Model):
	first_name = models.CharField(
		verbose_name = "First Name : ",
		max_length = 100,
		help_text = "First Name",
		blank = False,
	)
	last_name = models.CharField(
		verbose_name = "Last Name : ",
		max_length = 100,
		help_text = "Last Name",
		blank = True,
	)
	email = models.EmailField(
		verbose_name = "Email : ",
		help_text = "Email id of the candidate.",
		unique = True,
	)
	gender = models.CharField(
		verbose_name = "Gender : ",
		help_text = "Gender of the applicant.",
		choices = choices.gender_choices,
		default = "F",
		max_length = 6,
		blank = False,
		null = True,
	)
	nationality = models.CharField(
		verbose_name = "Nationality : ",
		choices = choices.countries,
		help_text = "Nationality of the applicant",
		max_length = 50,
		blank = False,
		default = "IND",
		null = True,
	)
	res_address = models.CharField(
		verbose_name = "Residential Address : ",
		help_text = "Residential Address of the applicant",
		max_length = 50,
		blank = False,
		null = True,
	)
	perm_address = models.CharField(
		verbose_name = "Permanent Address : ",
		help_text = "Permanent Address of the applicant",
		max_length = 50,
		blank = False,
		null = True,
	)
	experience = models.FloatField(
		help_text = "Total work experience : ",
		verbose_name = "Work Experience: ",
		default = 0,
		blank = False,
		null = True,
	)
	currency = models.CharField(
		verbose_name = "Currency : ",
		choices = choices.currencies,
		help_text = "Currency",
		blank = False,
		max_length = 30,
		default = "",
		null = True,
	)
	salary = models.IntegerField(
		verbose_name = "Salary : ",
		default = 0,
		blank = False,
		help_text = "Current Salary",
		null = True,
	)
	job_title = models.CharField(
		verbose_name = "Job Title : ",
		max_length = 50,
		help_text = "Current work title / Designation.",
		blank = False,
		null = True,
	)
	company = models.CharField(
		verbose_name = "Company : ",
		max_length = 50,
		help_text = "Name of the company currently working in.",
		blank = False,
		null = True,
	)
	dept = models.CharField(
		verbose_name = "Department : ",
		max_length = 50,
		help_text = "Department of the applicant.",
		blank = False,
		null = True,
	)
	skills = models.TextField(
		verbose_name = "Skills : ",
		blank = True,
		null = True,
		help_text = "Skills of the applicant. Use Comma seperated values."
	)
	edu_level = models.CharField(
		verbose_name = "Qualification : ",
		choices = choices.education,
		help_text = "Highest eductional qualification of the applicant",
		default = 'B',
		max_length = 9,
		blank = False,
		null = True,
	)
	course = models.CharField(
		verbose_name = "Course : ",
		max_length = 50,
		help_text = "Qualified in",
		blank = False,
		null = True,
	)
	specialisation = models.CharField(
		verbose_name = "Specialisations : ",
		max_length = 50,
		help_text = "Applicant's specialisation",
		blank = False,
		null = True,
	)
	institute = models.CharField(
		verbose_name = "Institute : ",
		max_length = 50,
		help_text = "The institute in which applicant earned the education",
		blank = False,
		null = True,
	)
	year_of_completion = models.IntegerField(
		verbose_name = "Year of completion:",
		blank = False,
		help_text = "Year of completing education",
		null = True,
	)
	country_of_edu = models.CharField(
		verbose_name = "Country of Education : ",
		choices = choices.countries,
		help_text = "Country of education",
		max_length = 50,
		blank = False,
		default = "",
		null = True,
	)
	dob = models.DateField(
		verbose_name = "Date of Birth : ",
		help_text = "Date of birth of the applicant",
		blank = False,
		null = True,
	)
	visa_status = models.CharField(
		verbose_name = "Visa Status : ",
		choices = choices.visa_statuses,
		default = 'NV',
		help_text = "Current status of the visa in the country",
		blank = False,
		max_length = 14,
		null = True,
	)
	visa_country = models.CharField(
		max_length = 50,
		choices = choices.countries,
		blank = False,
		null = True,
	)
	languages = models.CharField(
		verbose_name = "Languages known : ",
		help_text = "Languages the applicant is fluent in.",
		max_length = 50,
		blank = False,
		default = "",
		null = True,
	)
	marital_status = models.CharField(
		verbose_name = "Marital Status : ",
		choices = choices.married,
		max_length = 7,
		blank = False,
		default = 'Y',
		help_text = "Marital Status of the applicant",
		null = True,
	)
	driving_license = models.CharField(
		verbose_name = "Driving License : ",
		choices = choices.driving_license_status,
		help_text = "Do you have a driving license?",
		blank = False,
		max_length = 3,
		default = "N",
		null = True,
	)
	exp_remarks = models.CharField(
		verbose_name = "Experience Notes",
		max_length = 255,
		blank = False,
		null = True,
	)
	about = models.CharField(
		verbose_name = "About",
		max_length = 255,
		blank = False,
		null = True,
	)
	profile_photo = models.ImageField(
		verbose_name = "Profile Photo",
		upload_to = "profile_photos/candidate/",
		blank = True
	)
	certifications = models.CharField(
		max_length = 255,
		verbose_name = "Certifications",
		help_text = "Certifications of the candidate",
		blank = True,
		null = True,
	)
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete = models.CASCADE,
		editable = False,
	)
	
	def get_exp_month(self):
		year = int(self.experience)
		month = round((self.experience - year) * 12)
		return month
